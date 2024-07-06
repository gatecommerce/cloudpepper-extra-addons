from odoo import models, fields

class WhatsAppBatchingConfig(models.Model):
    _name = 'whatsapp.batching.config'
    _description = 'Configurazione Batching WhatsApp'

    name = fields.Char(string='Nome', required=True)
    use_batching = fields.Boolean(string='Usa Batching', default=True)
    batch_size = fields.Integer(string='Dimensione Batch', default=50)
