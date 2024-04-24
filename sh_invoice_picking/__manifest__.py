# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Manage Invoices From Picking",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Accounting",
    "summary": "Auto Invoice From Picking Bill From Picking Bill From Incoming Orders Bills From Shipment Invoice From Shipment Invoice From Delivery Order auto invoice on received products auto invoice validate from picking To Bill Picking To Invoice Odoo Separate Invoices From Delivery Order Separate Bills From Incoming Orders Separate Invoices From Picking Order Separate Bills From Picking Order invoice from incoming shipment Vendor bill from Incoming Shipment Customer Invoice from Delivery Order Vendor Bill from Delivery Order Generate Bill from Picking Generate Invoice from Picking Auto Invoice on received goods Automatic Invoice from Picking Automatic Bill from Picking Auto Invoice From Receipt Customer Invoice from Receipt Vendor Bill from Receipt Single Order from Delivery Order",
    "description": """Sometimes in business, we need to create direct invoices or bills from picking. you can manage direct invoices from the delivery order and you can do direct bills from incoming orders. so you don't need to waste your time to manage all. you can do direct invoice and bill.""",
    "version": "0.0.8",
    "depends": [
        "sale_management",
        "purchase",
        "stock",
        "account"
    ],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "security/sh_create_invoice_groups.xml",
        "views/stock_picking_views.xml",
        "views/account_move_views.xml",
        "wizard/sh_create_invoice_wizard_views.xml",
    ],
    "images": ["static/description/background.png", ],
    "license": "OPL-1",
    "auto_install": False,
    "installable": True,
    "price": 30,
    "currency": "EUR"
}
