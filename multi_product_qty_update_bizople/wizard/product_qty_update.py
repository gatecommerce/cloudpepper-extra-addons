# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Bizople Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api

class LocationFieldAdd(models.TransientModel):
    _inherit = "stock.change.product.qty"

    location_id = fields.Many2one('stock.location', 'Location', required=True, domain="[('usage', '=', 'internal')]")



class ProductQuantityUpdate(models.TransientModel):
    _name = "product.quantity.update"
    _description = "Product Quantity Update Wizard"

    line_ids = fields.One2many("product.quantity.update.line", "wizard_id", "Product Details")

    @api.model
    def default_get(self, fields):
        res = super(ProductQuantityUpdate, self).default_get(fields)
        active_ids = self.env.context.get("active_ids", [])
        line_ids = []
        for product_id in active_ids:
            product = self.env['product.product'].browse(product_id)
            line_ids.append([0, False, {
                'product_id': product_id,
                'product_name': product.display_name,
                'qty_avail': product.qty_available or 0.0
            }])
        res['line_ids'] = line_ids
        return res

    def action_update_quantity(self):
        company_user = self.env.user.company_id
        location_id = False
        warehouse = self.env['stock.warehouse'].search([('company_id', '=', company_user.id)], limit=1)
        if warehouse:
            location_id = warehouse.lot_stock_id.id
        for obj in self:
            for line in obj.line_ids:
                if line.qty_update:
                    wizard_id = self.env['stock.change.product.qty'].create({
                        'location_id': location_id,
                        'product_id': line.product_id.id,
                        'product_tmpl_id':line.product_id.product_tmpl_id.id,
                        'new_quantity': line.qty_update or 0.0
                    })
                    wizard_id.change_product_qty()
        return {'type': 'ir.actions.act_window_close'}


class ProductQuantityUpdateLines(models.TransientModel):
    _name = "product.quantity.update.line"
    _description = "Product Quantity Update Lines"

    wizard_id = fields.Many2one("product.quantity.update", "Wizard")
    product_id = fields.Many2one("product.product", "Product")
    product_name = fields.Char("Product Name")
    qty_avail = fields.Float("Quantity On Hand")
    qty_update = fields.Float("Quantity Update")
