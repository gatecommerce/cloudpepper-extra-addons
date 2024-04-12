# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Bizople Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Mass Product On Hand Quantity Update',
    'category': 'Sales',
    'version': '17.0.0.0',
    'author': 'Bizople Solutions Pvt. Ltd.',
    'sequence': 1,
    'website': 'https://www.bizople.com',
    'summary': 'Mass Product On Hand Quantity Update',
    'description': """Mass Product On Hand Quantity Update""",
    'depends': [
        'base',
        'stock',
        'sale_management',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/product_qty_update_view.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 10,
    'license': 'OPL-1',
    'currency': 'EUR',
}
