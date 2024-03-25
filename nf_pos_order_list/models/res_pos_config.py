# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api, _

class ResConfigPosInherit(models.TransientModel):
    _inherit = "res.config.settings"

    nf_pos_enable_order_list = fields.Boolean(related="pos_config_id.nf_pos_enable_order_list", readonly=False)
    nf_pos_order_limit_per_page = fields.Integer(related="pos_config_id.nf_pos_order_limit_per_page", readonly=False)