# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 


from odoo import models, fields, api, _
from odoo.tools import float_is_zero, float_round
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class PosOrder(models.Model):
    _inherit = 'pos.order'

    state = fields.Selection(selection_add=[('partial_paid', 'Partial Paid')])
    nf_is_partial_payment = fields.Boolean(string="is Partial Paid")
    nf_pos_order_reference_id = fields.Many2one('pos.order', string="Partial Order Reference") 
    
    @api.model
    def _process_order(self, order, draft, existing_order):
        pos_order =  super(PosOrder, self)._process_order(order, draft, existing_order)
        self_order = self.browse(pos_order)
        if order['data'].get('nf_is_partial_payment'):
            self_order.write({'state': 'partial_paid'})
        return pos_order

    @api.model
    def create_from_ui(self, orders, draft=False):
        results = super().create_from_ui(orders, draft)
        order_ids = []
        for order in orders:
            existing_draft_order = None

            if 'server_id' in order['data'] and order['data']['server_id']:
                # if the server id exists, it must only search based on the id
                existing_draft_order = self.env['pos.order'].search(['&', ('id', '=', order['data']['server_id']), ('state', '=', 'draft')], limit=1)

                # if there is no draft order, skip processing this order
                if not existing_draft_order:
                    print('\n\n\n >>>>> ')
                    pos_order = self.env['pos.order'].browse(order['data']['server_id'])
                    for payments in order['data']['statement_ids']:
                        pos_order.add_payment(self._payment_fields(pos_order, payments[2]))
                        if order['data']['nf_is_partial_payment']:
                            customer_account_payment_meth =  pos_order.payment_ids.filtered(lambda o: o.payment_method_id.split_transactions )
                            if customer_account_payment_meth:
                                payment_method_id = customer_account_payment_meth.payment_method_id.id
                                payments[2]['payment_method_id'] = payment_method_id,
                    pos_order.amount_paid = sum(pos_order.payment_ids.filtered(lambda o: not o.payment_method_id.split_transactions ).mapped('amount'))

                    if pos_order.amount_paid == pos_order.amount_total:
                        pos_order.write({'state': 'paid'})
            else:
                ids = list(map(lambda x: x.get('id'), results))
                pos_orders = self.search([('id', 'in', ids)])
                for pos_order in pos_orders:
                    pos_order.amount_paid = sum(pos_order.payment_ids.filtered(lambda o: not o.payment_method_id.split_transactions ).mapped('amount'))


        return results

    @api.model
    def _payment_fields(self, order, ui_paymentline):
        res = super()._payment_fields(order, ui_paymentline)
        if ui_paymentline.get('session_id'):
            res['session_id'] = ui_paymentline.get('session_id')
        if ui_paymentline.get('nf_partial_payment_session_id'):
            res['nf_partial_payment_session_id'] = ui_paymentline.get('nf_partial_payment_session_id')
        return res 

    @api.model
    def nf_search_partial_orders(self):
        allOrders = self.search_read([])
        retrunAllOrders = list(filter(lambda order: (order.get('amount_total') - order.get('amount_paid')) > 1, allOrders))
        return retrunAllOrders

class PosSessionInherit(models.Model):
    _inherit = 'pos.session'

    nf_pos_partial_paid_payment_ids = fields.One2many('pos.payment', 'session_id', string="partial paid orders ")
    
    def _loader_params_res_partner(self):
        result = super()._loader_params_res_partner()
        result['search_params']['fields'].extend(['credit', 'nfAccountDue'])
        return result
    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        result['search_params']['fields'].append('is_partial_paid_product')
        return result

class PosPayment(models.Model):
    _inherit = 'pos.payment'

    nf_partial_payment_session_id = fields.Many2one('pos.session', string="Partail Payment Session")