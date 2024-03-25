# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api

class PosConfig(models.Model):
    _inherit = 'pos.config'

    nf_enbale_price_discount = fields.Boolean(string="Enable Global Discount ? ")