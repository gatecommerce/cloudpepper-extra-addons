# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class QuotationOrderLine(models.Model):
    _inherit = 'sale.order.line'

    so_order_date = fields.Datetime(
        related="order_id.date_order",
        string="Date Order"
    )
    so_state = fields.Selection(
        related="order_id.state",
        string="State",
        store=True
    )

    image = fields.Image(string=" ", compute='_compute_image')
    sh_remaining_delivered_qty=fields.Float('Remaining Delivery Quantity' ,compute='_compute_remaining_delivery_qty')
    sh_remaining_delivered_amount=fields.Float('Remaining Delivery Amount',compute='_compute_remaining_delivery_amt')
    sh_remaining_invoice_qty=fields.Float('Remaining invoice Quantity' ,compute='_compute_remaining_invoice_qty')
    sh_remaining_invoice_amount=fields.Float('Remaining invoice Amount' ,compute='_compute_remaining_invoice_amt')

    invoice_remaining=fields.Boolean('Invoice Remaining',default=False)

    def _compute_remaining_delivery_qty(self):
        for rec in self:
            if rec.product_uom_qty:
                rec.sh_remaining_delivered_qty= rec.product_uom_qty - rec.qty_delivered
            else:
                rec.sh_remaining_delivered_qty=0

    def _compute_remaining_delivery_amt(self):
        for rec in self:
            if rec.sh_remaining_delivered_qty and rec.price_unit:
                rec.sh_remaining_delivered_amount=rec.sh_remaining_delivered_qty * rec.price_unit
            else:
                rec.sh_remaining_delivered_amount=0

    def _compute_remaining_invoice_qty(self):
        for rec in self:
            if rec.product_uom_qty:
                rec.sh_remaining_invoice_qty= rec.product_uom_qty - rec.qty_invoiced
            else:
                rec.sh_remaining_invoice_qty=0

    def _compute_remaining_invoice_amt(self):
        for rec in self:
            if rec.sh_remaining_invoice_qty and rec.price_unit:
                rec.sh_remaining_invoice_amount=rec.sh_remaining_invoice_qty * rec.price_unit
                rec.invoice_remaining=True
            else:
                rec.sh_remaining_invoice_amount=0
                rec.invoice_remaining=False


    def _compute_image(self):
        """Get the image from the template if no image is set on the variant."""
        for record in self:
            record.image = record.product_id.image_variant_1920 or record.product_id.product_tmpl_id.image_1920

    def action_get_quotation(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Quotation",
            "view_mode": "form",
            "res_model": "sale.order",
            "res_id": self.order_id.id
        }

    def action_get_sale_order(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Sale Order",
            "view_mode": "form",
            "res_model": "sale.order",
            "res_id": self.order_id.id
        }


    @api.onchange('order_id')
    def _onchange_order_id(self):
        self.ensure_one()
        if self.order_id:
            if not self.order_id.state in ('draft', 'senf'):
                raise UserError(_("Selected Order Must Be In 'Quotation' or 'Quotation Sent' State To Create Its Order Line!"))