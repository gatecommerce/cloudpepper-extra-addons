# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import base64
import json


class ImportDataWizard(models.TransientModel):
    _name = 'import.data.wizard'
    _description = "import Data wizard"

    add_attachment = fields.Binary(string="Order's JSON File", attachment=True, required=True)

    def import_data_with_create_order(self):
        my_json = self.add_attachment.decode('utf8').replace("'", '"')
        base64_bytes = my_json.encode("ascii")
        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii")
        final_data = json.loads(sample_string)
        pos_order_obj = self.env['pos.order']
        pos_order_obj.create_from_ui(final_data)
        all_created_object = self.env['order.data'].search([])
        create_data_obj = self.env['order.data']
        for order_data in final_data:
            order_data1 = order_data.get('data')
            flag = True
            for all_created_id in all_created_object:
                if all_created_id.name == order_data1['name']:
                    flag = False
                    raise ValidationError(_('Orders allready imported.'))
            if flag:
                create_data_obj.create({'name': order_data1['name'], 'order_JSON': order_data,
                    'result': 'Your Order Is Successfully Created.', 'state': 'done'})

    def import_data(self):
        my_json = self.add_attachment.decode('utf8').replace("'", '"')
        base64_bytes = my_json.encode("ascii")
        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii")
        final_data = json.loads(sample_string)
        all_created_object = self.env['order.data'].search([])
        create_data_obj = self.env['order.data']
        for order_data in final_data:
            order_data1 = order_data.get('data')
            flag = True
            for all_created_id in all_created_object:
                if all_created_id.name == order_data1['name']:
                    flag = False
                    raise ValidationError(_('Orders allready imported.'))
            if flag:
                create_data_obj.create({'name': order_data1['name'], 'order_JSON': order_data,
                    'result': '', 'state': 'open'})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: