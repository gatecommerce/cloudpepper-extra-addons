from odoo import fields, models


class ProductList(models.Model):
    _name = "product.list"
    _description = "Product for interactive"

    product_retailer_id = fields.Char(string="Product Retailer")
    interactive_product_list_id = fields.Many2one(
        comodel_name="interactive.product.list"
    )


class ProductListTitle(models.Model):
    _name = "interactive.product.list"
    _description = "Product list"

    main_title = fields.Char(string="Title")
    wa_interactive_id = fields.Many2one(comodel_name="wa.interactive.template")
    product_list_ids = fields.One2many(
        comodel_name="product.list",
        inverse_name="interactive_product_list_id",
        string="Product Items",
    )
