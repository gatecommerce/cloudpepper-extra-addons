# -*- coding: utf-8 -*-
# Part of Softhealer Technologies

from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    remarks_for_purchase = fields.Text(
        string="Remarks for Purchase", related="move_id.remarks_for_purchase")
    is_remarks_for_purchase = fields.Boolean(
        related="company_id.remark_for_purchase_order", string="Is Remarks for Purchase")
