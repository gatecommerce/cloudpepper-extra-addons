# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.exceptions import UserError
from odoo.http import request


class HideVariant(http.Controller):
    @http.route("/get_product_variant_data_website", type="json", website=True, methods=['POST'], auth="public")
    def get_product_variant_data(self, product_tmpl_id=None):
        product_tmpl_id = request.env["product.template"].search([("id", "=", product_tmpl_id)])
        if product_tmpl_id:
            return product_tmpl_id.get_variant_count()
