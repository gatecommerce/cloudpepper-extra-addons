# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api, _ 

class PosConfigInherit(models.Model):
    _inherit = 'pos.config'

    _nf_pos_enable_partial_payment = fields.Boolean(string="Enable Partial Payment ? ")
    nf_partial_payment_product = fields.Many2one('product.product', string="Product")

    def _get_special_products(self):
        results = super()._get_special_products()
        partial_payment_service_product = self.env.ref('nf_pos_partial_payment.nf_product_product_service_product', raise_if_not_found=False) or self.env['product.product']
        return results | partial_payment_service_product

class PosCustomerInherit(models.Model):
    _inherit = "res.partner"

    nfAccountDue = fields.Float(string="due amount")
