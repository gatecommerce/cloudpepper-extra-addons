# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api, _

class ResConfigPosInherit(models.TransientModel):
    _inherit = "res.config.settings"

    _nf_pos_enable_partial_payment = fields.Boolean(related="pos_config_id._nf_pos_enable_partial_payment", readonly=False)
    nf_partial_payment_product = fields.Many2one(related="pos_config_id.nf_partial_payment_product", readonly=False)