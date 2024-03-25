# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api, _

class PosSessoin(models.Model):
    _inherit = "pos.session"


    def _pos_data_process(self, loaded_data):
        super()._pos_data_process(loaded_data)
        
