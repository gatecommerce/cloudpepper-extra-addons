# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Product Brand Management",
    "author": "Softhealer Technologies",
    "website": "http://www.softhealer.com",
    "support": "support@softhealer.com",
    "license": "OPL-1",
    "category": "Productivity",
    "summary": "Manage Brand Products Search Brand Wise Product Filter Product By Brand Select Brand Product Group By Product Brands Choose Brand Product Get Particular Brand Product Assign Products Brand Odoo",
    "description": """Do you want to get brand-wise products? Currently, in odoo, you can"t manage products by brands. This module allows for managing product brands. It also helps to search, filter and group by-products by brand, it also shows how many products in a particular brand.""",
    "version": "0.0.2",
    "depends": [
        "sale_management",
    ],
    "application": True,
    "data": [
        "security/sh_product_brand_security.xml",
        "security/ir.model.access.csv",
        "views/sh_product_brand_views.xml",
        "views/product_views.xml",
        "views/sale_views.xml",
    ],
    "images": ["static/description/background.png"],
    "auto_install": False,
    "installable": True,
    "price": 20,
    "currency": "EUR",
}
