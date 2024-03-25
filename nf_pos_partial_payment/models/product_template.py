# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api, _ 

class NfProductProduct(models.Model):
    _inherit = 'product.template'

    is_partial_paid_product = fields.Boolean(string="partial payment")

