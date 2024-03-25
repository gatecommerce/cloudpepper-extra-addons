# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).
{
    'name': 'Purchase Return',
    'version': '17.0.1.0',
    'license': 'OPL-1',
    'category': 'Inventory/Purchase',
    'author': 'Kanak Infosystems LLP.',
    'website': 'https://kanakinfosystems.com',
    "summary": '''
        Purchase Return Module allows user to efficiently track and manage purchase order along with their delivery returns, user can return products from purchase order itself without interacting with stock picking. | Purchase Return | Return Order | Purchase Picking | In Picking | Return Picking | Return Purchase Order
    ''',
    'description': '''
        Using this Module user can return Purchase order directly from purchase and stocks are managed automatically.
        Return products from purchase order directly.
        Stock gets updated automatically.
        Picks gets created automatically.
        Track previous returns from return history.
        Can Return Multiple products at a time from current purchase order.
    ''',
    'depends': [
        'stock',
        'purchase',
        'utm'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/return_sequence_data.xml',
        'wizard/knk_purchase_return_wizard_views.xml',
        'views/purchase_order_return_views.xml',
        'views/purchase_views.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'currency': 'EUR',
    'price': 30,
}
