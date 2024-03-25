# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OrderData(models.Model):
    _name = "order.data"
    _description = "Order Data"

    name = fields.Char(string='Name', readonly=True)
    order_JSON = fields.Text(string="Order JSON", readonly=True)
    state = fields.Selection([('open', 'Open'), ('cancel', 'Cancel'), ('done', 'Done')],
                       string='Status')
    result = fields.Text(string="Results :- ", readonly=True)

    def create_order(self):
        final_data_list = []
        order_data = str(self.order_JSON)
        final_data = eval(order_data)
        data_dict = final_data.get('data')
        pos_order_obj = self.env['pos.order'].search([('pos_reference', '=', data_dict.get('name'))])
        if not pos_order_obj:
            final_data_list.append(final_data)
            pos_order_obj_added = self.env['pos.order']
            pos_order_obj_added.create_from_ui(final_data_list)
            self.state = 'done'
            self.result = 'Your Order Is Successfully Created.'
        else:
            raise ValidationError(
                _('Orders allready created.'))

    def cancel_order(self):
        self.state = 'cancel'

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: