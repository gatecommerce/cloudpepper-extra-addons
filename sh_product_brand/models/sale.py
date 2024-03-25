# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    sh_brand_id = fields.Many2one(
        "sh.product.brand", string="Brand", related="product_id.sh_brand_id", store=True)


class SaleOrder(models.Model):
    _inherit = "sale.report"

    sh_brand_id = fields.Many2one(
        "sh.product.brand", string="Brand", readonly=True)

    def _select_additional_fields(self):
        res = super(SaleOrder,self)._select_additional_fields()
        res['sh_brand_id'] = "l.sh_brand_id"
        return res

    def _group_by_sale(self):
        res = super(SaleOrder,self)._group_by_sale()
        res += """,
            l.sh_brand_id"""
        return res