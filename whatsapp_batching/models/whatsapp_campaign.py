import logging
from odoo import models, fields, api  # Aggiungi questa riga per importare correttamente models, fields, e api

_logger = logging.getLogger(__name__)

class WhatsAppCampaign(models.Model):
    _inherit = 'whatsapp.messaging.lists'

    processed_contacts = fields.Integer(string='Contatti Processati', default=0)

    def _send_campaign_messages_in_batches(self):
        self.ensure_one()
        if not self.batching_config_id or not self.batching_config_id.use_batching:
            return super()._send_campaign_messages_in_batches()

        batch_size = self.batching_config_id.batch_size
        total_contacts = len(self.contact_ids)
        start = self.processed_contacts
        end = min(start + batch_size, total_contacts)

        _logger.info(f"Inizio invio batch per campagna {self.name}. Contatti {start+1} - {end} di {total_contacts}")

        try:
            for contact in self.contact_ids[start:end]:
                self._send_message_to_contact(contact)
                self.processed_contacts += 1
                if self.processed_contacts % 10 == 0:  # Commit ogni 10 messaggi per migliorare le prestazioni
                    self.env.cr.commit()

            self.env.cr.commit()  # Commit finale per salvare eventuali progressi restanti

        except Exception as e:
            _logger.error(f"Errore durante l'invio dei messaggi: {str(e)}")
            self.env.cr.rollback()  # Rollback in caso di errore

        _logger.info(f"Fine invio batch per campagna {self.name}. Processati {self.processed_contacts} contatti su {total_contacts}")

        if self.processed_contacts < total_contacts:
            self._schedule_next_batch()
        else:
            _logger.info(f"Campagna {self.name} completata. Tutti i {total_contacts} contatti sono stati processati.")

    def _schedule_next_batch(self):
        interval_minutes = 5  # Potrebbe essere configurabile
        self.env['ir.cron'].sudo().create({
            'name': f'Prossimo batch per campagna {self.name}',
            'model_id': self.env['ir.model'].search([('model', '=', self._name)]).id,
            'state': 'code',
            'code': f'env["{self._name}"].browse({self.id})._send_campaign_messages_in_batches()',
            'interval_number': interval_minutes,
            'interval_type': 'minutes',
            'numbercall': 1,
            'doall': True,
        })
        _logger.info(f"Schedulato prossimo batch per campagna {self.name} tra {interval_minutes} minuti")
