# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class InvoiceLine(models.Model):
    _inherit = 'account.move.line'

    state = fields.Selection(
        related="move_id.state",
        string="State",
        store=True
    )
    inv_type = fields.Selection(
        related="move_id.move_type",
        string="Type ",
        store=True
    )
    sh_payment_state = fields.Selection(
        related="move_id.payment_state",
        string="Payment Status ",
        store=True
    )

    image = fields.Image(string=" ", compute='_compute_image')

    def _compute_image(self):
        """Get the image from the template if no image is set on the variant."""
        for record in self:
            record.image = record.product_id.image_variant_1920 or record.product_id.product_tmpl_id.image_1920

    def action_invoice(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Invoice",
            "view_mode": "form",
            "res_model": "account.move",
            "res_id": self.move_id.id
        }
