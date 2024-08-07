import json
import logging
import threading

import markupsafe
import requests

from odoo import Command, _, models
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from odoo.tools import groupby

from odoo.addons.whatsapp.tools.whatsapp_api import WhatsAppApi
from odoo.addons.whatsapp.tools.whatsapp_exception import WhatsAppError

_logger = logging.getLogger(__name__)
DEFAULT_ENDPOINT = "https://graph.facebook.com/v17.0"


class WhatsappMessage(models.Model):
    _inherit = "whatsapp.message"

    def _api_requests_interactive(
        self,
        request_type,
        url,
        auth_type="",
        params=False,
        headers=None,
        data=False,
        files=False,
        endpoint_include=False,
    ):
        if getattr(threading.current_thread(), "testing", False):
            raise WhatsAppError("API requests disabled in testing.")

        headers = headers or {}
        params = params or {}
        if not all([self.wa_account_id.token, self.wa_account_id.phone_uid]):
            action = self.wa_account_id.env.ref("whatsapp.whatsapp_account_action")
            raise RedirectWarning(
                _("To use WhatsApp Configure it first"),
                action=action.id,
                button_text=_("Configure Whatsapp Business Account"),
            )
        if auth_type == "oauth":
            headers.update({"Authorization": f"OAuth {self.wa_account_id.token}"})
        if auth_type == "bearer":
            headers.update({"Authorization": f"Bearer {self.wa_account_id.token}"})
        call_url = (DEFAULT_ENDPOINT + url) if not endpoint_include else url

        try:
            res = requests.request(
                request_type,
                call_url,
                params=params,
                headers=headers,
                data=data,
                files=files,
                timeout=10,
            )
        except requests.exceptions.RequestException:
            raise WhatsAppError(failure_type="network")

        # raise if json-parseable and 'error' in json
        try:
            if "error" in res.json():
                raise WhatsAppError(
                    *self._prepare_error_response_interactive(res.json())
                )
        except ValueError:
            if not res.ok:
                raise WhatsAppError(failure_type="network")

        return res

    def _prepare_error_response_interactive(self, response):
        """
        This method is used to prepare error response
        :return tuple[str, int]: (error_message, whatsapp_error_code | -1)
        """
        if response.get("error"):
            error = response["error"]
            desc = error.get("message", "")
            desc += (
                (" - " + error["error_user_title"])
                if error.get("error_user_title")
                else ""
            )
            desc += (
                ("\n\n" + error["error_user_msg"])
                if error.get("error_user_msg")
                else ""
            )
            code = error.get("code", "odoo")
            return (desc if desc else _("Non-descript Error"), code)
        return (
            _(
                "Something went wrong when contacting WhatsApp, please try again later. If this happens frequently, contact support."
            ),
            -1,
        )

    def _send_whatsapp_interactive(
        self, number, message_type, send_vals, parent_message_id=False
    ):
        """Send WA messages for all message type using WhatsApp Business Account

        API Documentation:
            Normal        - https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages
            Template send - https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates
        """
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
        }
        # if there is parent_message_id then we send message as reply
        if parent_message_id:
            data.update(
                {
                    "context": {"message_id": parent_message_id},
                }
            )
        if message_type in (
            "template",
            "text",
            "document",
            "image",
            "audio",
            "video",
            "interactive",
        ):
            data.update({"type": message_type, message_type: send_vals})
        json_data = json.dumps(data)
        _logger.info(
            "Send %s message from account %s [%s]",
            message_type,
            self.wa_account_id.name,
            self.wa_account_id.id,
        )
        response = self._api_requests_interactive(
            "POST",
            f"/{self.wa_account_id.phone_uid}/messages",
            auth_type="bearer",
            headers={"Content-Type": "application/json"},
            data=json_data,
        )
        response_json = response.json()
        if response_json.get("messages"):
            msg_uid = response_json["messages"][0]["id"]
            return msg_uid
        raise WhatsAppError(*self._prepare_error_response_interactive(response_json))

    def _send_message(self, with_commit=False):
        """Prepare json data for sending messages, attachments and templates."""
        # init api
        message_to_api = {}
        for account, messages in groupby(self, lambda msg: msg.wa_account_id):
            if not account:
                messages = self.env["whatsapp.message"].concat(*messages)
                messages.write(
                    {
                        "failure_type": "unknown",
                        "failure_reason": "Missing whatsapp account for message.",
                        "state": "error",
                    }
                )
                self -= messages
                continue
            wa_api = WhatsAppApi(account)
            for message in messages:
                message_to_api[message] = wa_api

        for whatsapp_message in self:
            whatsapp_message = whatsapp_message.with_user(whatsapp_message.create_uid)
            try:
                parent_message_id = False
                body = whatsapp_message.body
                if isinstance(body, markupsafe.Markup):
                    # If Body is in html format so we need to remove html tags before sending message.
                    body = body.striptags()
                number = whatsapp_message.mobile_number_formatted
                if not number:
                    raise WhatsAppError(failure_type="phone_invalid")
                if (
                    self.env["phone.blacklist"]
                    .sudo()
                    .search([("number", "ilike", number)])
                ):
                    raise WhatsAppError(failure_type="blacklisted")
                if (
                    whatsapp_message.wa_template_id
                    and whatsapp_message.wa_template_id.template_category
                    == "interactive"
                ):
                    message_type = "interactive"
                    if (
                        whatsapp_message.wa_template_id.status != "approved"
                        or whatsapp_message.wa_template_id.quality in ("red", "yellow")
                    ):
                        raise WhatsAppError(failure_type="template")
                    whatsapp_message.message_type = "outbound"
                    if (
                        whatsapp_message.mail_message_id.model
                        != whatsapp_message.wa_template_id.model
                    ):
                        raise WhatsAppError(failure_type="template")

                    RecordModel = self.env[
                        whatsapp_message.mail_message_id.model
                    ].with_user(whatsapp_message.create_uid)
                    from_record = RecordModel.browse(
                        whatsapp_message.mail_message_id.res_id
                    )
                    (
                        send_vals,
                        attachment,
                    ) = whatsapp_message.wa_template_id._get_send_template_vals(
                        record=from_record,
                        free_text_json=whatsapp_message.free_text_json,
                        attachment=whatsapp_message.mail_message_id.attachment_ids,
                    )
                    if attachment:
                        # If retrying message then we need to remove previous attachment and add new attachment.
                        if (
                            whatsapp_message.mail_message_id.attachment_ids
                            and whatsapp_message.wa_template_id.header_type
                            == "document"
                            and whatsapp_message.wa_template_id.report_id
                        ):
                            whatsapp_message.mail_message_id.attachment_ids.unlink()
                        if (
                            attachment
                            not in whatsapp_message.mail_message_id.attachment_ids
                        ):
                            whatsapp_message.mail_message_id.attachment_ids = [
                                Command.link(attachment.id)
                            ]
                else:
                    return super(WhatsappMessage, self)._send_message(with_commit=False)
                msg_uid = whatsapp_message._send_whatsapp_interactive(
                    number=number,
                    message_type=message_type,
                    send_vals=send_vals,
                    parent_message_id=parent_message_id,
                )
            except WhatsAppError as we:
                whatsapp_message._handle_error(
                    whatsapp_error_code=we.error_code,
                    error_message=we.error_message,
                    failure_type=we.failure_type,
                )
            except (UserError, ValidationError) as e:
                whatsapp_message._handle_error(
                    failure_type="unknown", error_message=str(e)
                )
            else:
                if not msg_uid:
                    whatsapp_message._handle_error(failure_type="unknown")
                else:
                    if message_type == "interactive":
                        whatsapp_message._post_message_in_active_channel()
                    whatsapp_message.write({"state": "sent", "msg_uid": msg_uid})
                if with_commit:
                    self._cr.commit()
