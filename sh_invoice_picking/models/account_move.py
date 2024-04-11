# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class ShAccountInvoice(models.Model):
    _inherit = 'account.move'

    sh_picking_ids = fields.Many2many('stock.picking','sh_picking_account_move_rel', string="Picking")
