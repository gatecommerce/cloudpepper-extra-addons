# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': 'Point Of Sale Partial Payment',
    'author': 'NextFlowIT',
    'category': "Point of sale",
    'summary': """ Manage Point of sale payments in partial payment pos partial payment point of sale partial payment payments get haff payment from customer show customer due amount customer credit display partial pos """,
    'description': """ 
Get partially Payment in point of sale 
=========================================

This module add functionality to get payment patrially from your valuable clients.

Key Features
------------
* Get partially payment from your client.
* Show client due amount on customer list screen.

 """,
    "license": "OPL-1",
    'website': '',
    'depends': ['point_of_sale','nf_pos_order_list'],
    'version': '0.0.1',
    'data': [
        'data/partial_payeent_product.xml',
        'views/pos_order.xml',
        'views/pos_config.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'nf_pos_partial_payment/static/src/overrides/models/*',
            'nf_pos_partial_payment/static/src/screens/order_list/*',
            'nf_pos_partial_payment/static/src/screens/PaymentScreen/*'
        ],
    },
    "images": ["static/description/background.gif", ],
    "price": 50.42,
    'installable': True,
    'application': True,
    'auto_install': False,
    "currency": "EUR"
}
