# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields

class PosConfig(models.Model):
    _inherit = "pos.config"

    nf_pos_enable_order_list = fields.Boolean(string="Enable order list ? ")
    nf_pos_order_limit_per_page = fields.Integer(string="Orders per page", default=30)
