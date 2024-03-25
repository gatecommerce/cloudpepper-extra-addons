# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name': "POS Order Backup & Restore",
    'version': '17.0.0.0',
    'category': 'Point of Sale',
    'summary': "POS backup orders restore the unsaved orders in POS download unsaved orders on POS restore orders on POS order data import restored POS order data backup point of sales order recovery on POS backup orders pos restore order from pos all orders backup",
    'description': """ 

        This Odoo App helps users to backup/restore the unsaved POS orders. User can easily download the unsaved orders in JSON format and import those JSON file to restore the orders. User can create POS order directly from restored orders data and also they have option to delete unsaved POS orders without downloading it.

    """,
    "author": "BrowseInfo",
    "price": 45,
    "currency": 'EUR',
    "website" : "https://www.browseinfo.com",
    'depends': ['base', 'point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/import_data_wizard.xml',
        'views/orders_data.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'bi_pos_order_restore/static/src/css/pos.css',
            'bi_pos_order_restore/static/src/app/MultiChoicePopup.js',
            'bi_pos_order_restore/static/src/app/MultiChoicePopup.xml',
            'bi_pos_order_restore/static/src/app/pos_state.js',
            'bi_pos_order_restore/static/src/app/pos_order.js',
            'bi_pos_order_restore/static/src/app/RestoreButton.js',
            'bi_pos_order_restore/static/src/app/RestoreButton.xml',
        ],
    },
    'license':'OPL-1',
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/Dub7oMfYzgs',
    "images":['static/description/POS-Order-Backup-Restore-Banner.gif'],
}
