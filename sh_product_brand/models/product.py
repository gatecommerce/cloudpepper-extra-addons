# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class ShProductTemplate(models.Model):
    _inherit = "product.template"

    sh_brand_id = fields.Many2one("sh.product.brand", string="Brand")
