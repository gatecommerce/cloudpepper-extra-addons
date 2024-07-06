{
    'name': 'WhatsApp Marketing Batching',
    'version': '17.0.1.0.0',
    'category': 'Marketing',
    'summary': 'Aggiunge funzionalità di invio in batch alle campagne WhatsApp',
    'description': """
        Questo modulo estende le funzionalità del modulo di marketing WhatsApp esistente,
        permettendo l'invio di messaggi in batch per evitare i limiti dell'API.
    """,
    'author': 'CRX',
    'website': 'https://www.cirax.it',
    'depends': ['base', 'tus_whatsapp_marketing_enterprise'],
    'data': [
        'security/ir.model.access.csv',
        'views/whatsapp_campaign_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}