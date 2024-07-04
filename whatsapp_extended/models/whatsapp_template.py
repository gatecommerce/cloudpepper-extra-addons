from odoo import _, api, fields, models
from odoo.exceptions import UserError


class WhatsappTemplate(models.Model):
    _inherit = "whatsapp.template"

    template_category = fields.Selection(
        [("template", "Template"), ("interactive", "Interactive")],
        string="Template Type",
    )

    wa_interactive_ids = fields.One2many(
        comodel_name="wa.interactive.template",
        inverse_name="wa_template_id",
        string="Interactive",
    )

    def button_set_status_to_added(self):
        for rec in self:
            rec.status = "approved"

    def _get_interactive_component(self):
        params = []
        for interactive in self.wa_interactive_ids:
            template_dict = {}
            template_dict.update({"type": interactive.interactive_type})
            if self.header_type == "text":
                header = {"type": self.header_type, "text": self.header_text}
                template_dict.update({"header": header})
            elif self.header_type in ["image", "video", "document"]:
                attachment = self.header_attachment_ids
                header = [
                    self.env["whatsapp.message"]._prepare_attachment_vals(
                        attachment, wa_account_id=self.wa_account_id
                    )
                ]
                # if self.header_type == 'document':
                #     header[0].get(self.header_type).update({'filename': attachment.name})
                template_dict.update({"header": header[0]})
            if self.body:
                body = {"text": self.body}
                template_dict.update({"body": body})
            if self.footer_text:
                footer = {"text": self.footer_text}
                template_dict.update({"footer": footer})
            if interactive.interactive_type == "product_list":
                if interactive.interactive_product_list_ids:
                    section = []
                    for product in interactive.interactive_product_list_ids:
                        product_items = []

                        for products in product.product_list_ids:
                            product_item = {
                                "product_retailer_id": products.product_retailer_id
                            }

                            product_items.append(product_item)

                        section.append(
                            {
                                "title": product.main_title,
                                "product_items": product_items,
                            }
                        )

                    action = {"catalog_id": interactive.catalog_id, "sections": section}

                    template_dict.update({"action": action})

            elif interactive.interactive_type == "button":
                if interactive.interactive_button_ids:
                    buttons = []
                    for btn_id in interactive.interactive_button_ids:
                        buttons.append(
                            {
                                "type": "reply",
                                "reply": {"id": btn_id.id, "title": btn_id.title},
                            }
                        )
                    action = {"buttons": buttons}

                    template_dict.update({"action": action})

            elif interactive.interactive_type == "list":
                if interactive.interactive_list_ids:
                    section = []
                    for list_id in interactive.interactive_list_ids:
                        rows = []
                        for lists in list_id.title_ids:
                            title_ids = {
                                "id": lists.id,
                                "title": lists.title,
                                "description": lists.description or "",
                            }
                            rows.append(title_ids)

                        section.append({"title": list_id.main_title, "rows": rows})
                    action = {"button": list_id.main_title, "sections": section}
                    template_dict.update({"action": action})

            elif interactive.interactive_type == "product":
                action = {
                    "catalog_id": interactive.catalog_id,
                    "product_retailer_id": interactive.product_retailer_id,
                }
                template_dict.update({"action": action})

            if bool(template_dict):
                params.append(template_dict)
        return params

    def _get_send_template_vals(self, record, free_text_json, attachment=False):
        temp_vals = {}
        attachment = {}
        if self.template_category == "interactive":
            interactive = self._get_interactive_component()
            if interactive:
                temp_vals.update(interactive[0])
            return temp_vals, attachment
        else:
            return super(WhatsappTemplate, self)._get_send_template_vals(
                record, free_text_json, attachment=False
            )

    @api.constrains("wa_interactive_ids")
    def _check_wa_interactive_ids(self):
        if len(self.wa_interactive_ids) > 1:
            raise UserError(
                _(
                    "Adding more than one interactive type in a template is not supported. Please revise the template accordingly."
                )
            )
        else:
            pass
