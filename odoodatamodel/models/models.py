from odoo import models, fields, api
# -*- coding: utf-8 -*-
import hashlib
import logging
import os
import requests
from ast import literal_eval
from odoo.exceptions import ValidationError






class Relationdatamodel(models.Model):
    _name = 'odoodatamodel.odoodatamodel'
    _description = 'odoodatamodel.odoodatamodel'

    def action_redirect(self):
        return {'type': 'ir.actions.act_url',
                'url': '/data-model'
                }


class MiniTableau(models.Model):
    _name = 'mini.tableau'
    _description = 'mini.tableau'

    user_query = fields.Char(string="User Query")
    report_name = fields.Char(string="Report Name")
    report_rows = fields.Char(string="Rows")
    report_columns = fields.Char(string="Columns")
    chart_type = fields.Char(string="Chart Type", default="None")
    name = fields.Char(string="User name")
    query = fields.Char(string="UQuery")
    # savedQueries = fields.Char(string="saved query")


class MiniTableauQueries(models.Model):
    _name = 'mini.tableau.query'
    _description = 'mini.tableau.query'

    query_val = fields.Char(string="Query")
    query_name = fields.Char(string="Query Name")
    # query_id = fields.Char(string="Query id")
