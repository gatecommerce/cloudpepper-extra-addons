# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    sh_invoice_status = fields.Selection(
        related="order_id.invoice_status",
        string="Billing Status ",
        store=True
    )

    image = fields.Image(string=" ", compute='_compute_image')

    sh_remaining_received_qty=fields.Float('Remaining Received Quantity ' ,compute='_compute_remaining_delivery_qty')
    sh_remaining_received_amount=fields.Float('Remaining Received Amount ',compute='_compute_remaining_delivery_amt')
    sh_remaining_bill_qty=fields.Float('Remaining Bill Quantity' ,compute='_compute_remaining_bill_qty')
    sh_remaining_bill_amount=fields.Float('Remaining Bill Amount' ,compute='_compute_remaining_bill_amt')

    bill_remaining=fields.Boolean('Bill Remaining',default=False)

    def _compute_remaining_delivery_qty(self):
        for rec in self:
            if rec.product_uom_qty:
                rec.sh_remaining_received_qty= rec.product_uom_qty - rec.qty_received
            else:
                rec.sh_remaining_received_qty=0

    def _compute_remaining_delivery_amt(self):
        for rec in self:
            if rec.sh_remaining_received_qty and rec.price_unit:
                rec.sh_remaining_received_amount=rec.sh_remaining_received_qty * rec.price_unit
            else:
                rec.sh_remaining_received_amount=0

    def _compute_remaining_bill_qty(self):
        for rec in self:
            if rec.product_uom_qty:
                rec.sh_remaining_bill_qty= rec.product_uom_qty - rec.qty_invoiced
            else:
                rec.sh_remaining_bill_qty=0

    def _compute_remaining_bill_amt(self):
        for rec in self:
            if rec.sh_remaining_bill_qty and rec.price_unit:
                rec.sh_remaining_bill_amount=rec.sh_remaining_bill_qty * rec.price_unit
                rec.bill_remaining=True
            else:
                rec.sh_remaining_bill_amount=0
                rec.bill_remaining=False

    def _compute_image(self):
        """Get the image from the template if no image is set on the variant."""
        for record in self:
            record.image = record.product_id.image_variant_1920 or record.product_id.product_tmpl_id.image_1920

    def action_get_purchse_order(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Purchase Order",
            "view_mode": "form",
            "res_model": "purchase.order",
            "res_id": self.order_id.id
        }

    def action_get_quotation(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Purchase Order",
            "view_mode": "form",
            "res_model": "purchase.order",
            "res_id": self.order_id.id
        }

    def _compute_price_unit_and_date_planned_and_name(self):
        for pol in self:
            print("\n\n\n>>> pol.company_id: ", pol.company_id, self.env.user.company_id,  pol.date_order)
            if not pol.company_id:
                pol.company_id = self.env.user.company_id.id
                pol.date_order = datetime.now()
        super(PurchaseOrderLine, self)._compute_price_unit_and_date_planned_and_name()

    @api.onchange('order_id')
    def _onchange_order_id(self):
        self.ensure_one()
        if self.order_id:
            if not self.order_id.state in ('draft', 'senf'):
                raise UserError(_("Selected Order Must Be In 'RFQ' or 'RFQ Sent' State To Create Its Order Line!"))