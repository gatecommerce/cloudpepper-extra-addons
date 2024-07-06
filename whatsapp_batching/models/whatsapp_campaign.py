import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class WhatsAppCampaign(models.Model):
    _inherit = 'whatsapp.messaging.lists'

    batching_config_id = fields.Many2one('whatsapp.batching.config', string='Batching Configuration')
    use_batching = fields.Boolean(string='Use Batching', default=True, readonly=True)
    batch_size = fields.Integer(string='Batch Size', default=50, readonly=True)
    processed_contacts = fields.Integer(string='Contatti Processati', default=0)

    @api.onchange('batching_config_id')
    def _onchange_batching_config_id(self):
        if self.batching_config_id:
            self.use_batching = self.batching_config_id.use_batching
            self.batch_size = self.batching_config_id.batch_size
        else:
            self.use_batching = False
            self.batch_size = 0

    def _send_campaign_messages_in_batches(self):
        self.ensure_one()
        if not self.batching_config_id or not self.batching_config_id.use_batching:
            return super()._send_campaign_messages_in_batches()

        batch_size = self.batching_config_id.batch_size
        total_contacts = len(self.contact_ids)
        start = self.processed_contacts
        end = min(start + batch_size, total_contacts)

        _logger.info(f"Inizio invio batch per campagna {self.name}. Contatti {start+1} - {end} di {total_contacts}")

        for contact in self.contact_ids[start:end]:
            self._send_message_to_contact(contact)
            self.processed_contacts += 1
            self.env.cr.commit()  # Commit after each message to save progress

        _logger.info(f"Fine invio batch per campagna {self.name}. Processati {self.processed_contacts} contatti su {total_contacts}")

        if self.processed_contacts < total_contacts:
            self._schedule_next_batch()
        else:
            _logger.info(f"Campagna {self.name} completata. Tutti i {total_contacts} contatti sono stati processati.")

    def _schedule_next_batch(self):
        self.env['ir.cron'].sudo().create({
            'name': f'Prossimo batch per campagna {self.name}',
            'model_id': self.env['ir.model'].search([('model', '=', self._name)]).id,
            'state': 'code',
            'code': f'env["{self._name}"].browse({self.id})._send_campaign_messages_in_batches()',
            'interval_number': 5,
            'interval_type': 'minutes',
            'numbercall': 1,
            'doall': True,
        })
        _logger.info(f"Schedulato prossimo batch per campagna {self.name} tra 5 minuti")
