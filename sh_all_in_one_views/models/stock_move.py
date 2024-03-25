# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.


from odoo import models, fields


class StockMove(models.Model):
    _inherit = "stock.move"

    sh_pol_picking_order_line_picking_type_id = fields.Many2one(
        comodel_name="stock.picking.type",
        related="picking_id.picking_type_id",
        ondelete='set null',
        store=True,
        string="Picking Type",
    )

    sh_pol_picking_order_line_picking_type_code = fields.Selection(
        related="picking_id.picking_type_id.code",
        store=True,
        string="Picking Operation",
    )

    image = fields.Image(string=" ", compute='_compute_image')

    def _compute_image(self):
        """Get the image from the template if no image is set on the variant."""
        for record in self:
            record.image = record.product_id.image_variant_1920 or record.product_id.product_tmpl_id.image_1920

    def action_transfer(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Transfer",
            "view_mode": "form",
            "res_model": "stock.picking",
            "res_id": self.picking_id.id
        }


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    sh_pol_picking_order_line_picking_type_id = fields.Many2one(
        comodel_name="stock.picking.type",
        related="picking_id.picking_type_id",
        ondelete='set null',
        store=True,
        string="Picking Type",
    )

    sh_pol_picking_order_line_picking_type_code = fields.Selection(
        related="picking_id.picking_type_id.code",
        store=True,
        string="Picking Operation",
    )
    sh_pol_picking_order_line_origin = fields.Char(
        related="picking_id.origin",
        store=True,
    )

    image = fields.Image(string=" ", compute='_compute_image')

    def _compute_image(self):
        """Get the image from the template if no image is set on the variant."""
        for record in self:
            record.image = record.product_id.image_variant_1920 or record.product_id.product_tmpl_id.image_1920

    def action_stock_move_line(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Transfer",
            "view_mode": "form",
            "res_model": "stock.move.line",
            "res_id": self.move_id.id
        }
