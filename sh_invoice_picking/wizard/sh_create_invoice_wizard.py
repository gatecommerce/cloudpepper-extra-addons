# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ShCreateInvoiceWizard(models.TransientModel):
    _name = 'sh.create.invoice.wizard'
    _description = "Create Invoice Wizard"

    @api.model
    def default_get(self, fields_list):
        rec = super(ShCreateInvoiceWizard, self).default_get(fields_list)
        active_ids = self._context.get('active_ids')
        journals = []
        if active_ids:
            first_type = self.env['stock.picking'].browse(
                active_ids[0]).picking_type_id.code
            for picking in active_ids:
                picking_id = self.env['stock.picking'].browse(picking)
                if picking_id.picking_type_id.code != first_type:
                    raise UserError(_("Please select same Type of Picking"))
            if first_type == 'incoming':
                journal_ids = self.env['account.journal'].search(
                    [('type', '=', 'purchase')])
                if journal_ids:
                    for journal_id in journal_ids:
                        journals.append(journal_id.id)
            if first_type == 'outgoing':
                journal_ids = self.env['account.journal'].search(
                    [('type', '=', 'sale')])
                if journal_ids:
                    for journal_id in journal_ids:
                        journals.append(journal_id.id)
        rec.update({
            'journal_ids': [(6, 0, journals)],
        })
        return rec

    sh_journal_id = fields.Many2one(
        'account.journal', string="Journal", required=True)
    sh_invoice_date = fields.Date(
        string="Invoice Date", default=fields.Date.today())
    sh_separate_invoice = fields.Boolean(string="Separate Invoice ?")
    journal_ids = fields.Many2many('account.journal', string="Journals")

    def action_create_invoices(self):
        active_ids = self.env.context.get('active_ids')
        # Code for inside picking form create invoice
        if len(active_ids) == 1 or self.sh_separate_invoice:
            for picking in active_ids:
                picking_id = self.env['stock.picking'].browse(picking)
                invoice_vals = {}
                # =====================================
                # Invoice Create
                # =====================================
                invoice_id = False
                if picking_id.picking_type_id.code == 'incoming' and self.sh_journal_id.type == 'purchase':
                    invoice_vals = {
                        'partner_id': picking_id.partner_id.id,
                        'user_id': self.env.user.id,
                        'invoice_date': self.sh_invoice_date,
                        'move_type': 'in_invoice',
                        'journal_id': self.sh_journal_id.id,
                        'sh_picking_ids': [(4, picking_id.id)],
                    }
                    invoice_id = self.env['account.move'].sudo().with_context(
                        default_move_type='in_invoice').create(invoice_vals)
                if picking_id.picking_type_id.code == 'outgoing' and self.sh_journal_id.type == 'sale':
                    invoice_vals = {
                        'partner_id': picking_id.partner_id.id,
                        'user_id': self.env.user.id,
                        'invoice_date': self.sh_invoice_date,
                        'move_type': 'out_invoice',
                        'journal_id': self.sh_journal_id.id,
                        'sh_picking_ids': [(4, picking_id.id)],
                    }
                    invoice_id = self.env['account.move'].sudo().with_context(
                        default_move_type='out_invoice').create(invoice_vals)
                for picking_line in picking_id.move_ids_without_package:
                    accounts = picking_line.product_id.product_tmpl_id.get_product_accounts(
                        invoice_id.fiscal_position_id)
                    if not accounts:
                        raise UserError(
                            _("No account defined for this product: " + picking_line.product_id.name))
                    invoice_line_vals = {}
                    # =====================================
                    # Invoice Line Create
                    # =====================================
                    if self.sh_journal_id.type == 'purchase':
                        invoice_line_vals = {
                            'product_id': picking_line.product_id.id,
                            'name': picking_line.product_id.name,
                            'quantity': picking_line.quantity,
                            'price_unit': picking_line.purchase_line_id.price_unit,
                            'tax_ids': [(6, 0, picking_line.purchase_line_id.taxes_id.ids)],
                            'move_id': invoice_id.id,
                            'account_id': accounts['expense'].id,
                        }
                    elif self.sh_journal_id.type == 'sale':
                        invoice_line_vals = {
                            'product_id': picking_line.product_id.id,
                            'name': picking_line.product_id.name,
                            'quantity': picking_line.quantity,
                            'price_unit': picking_line.sale_line_id.price_unit,
                            'tax_ids': [(6, 0, picking_line.sale_line_id.tax_id.ids)],
                            'move_id': invoice_id.id,
                            'account_id': accounts['income'].id,
                        }
                    invoice_line_id = self.env['account.move.line'].with_context(
                        check_move_validity=False).create(invoice_line_vals)

                    if picking_line.sale_line_id:
                        picking_line.sale_line_id.invoice_lines = [
                            (4, invoice_line_id.id)]

                    if picking_line.purchase_line_id:
                        picking_line.purchase_line_id.with_context(
                            check_move_validity=False).invoice_lines = [
                            (4, invoice_line_id.id)]

                if picking_id.purchase_id:
                    picking_id.purchase_id.invoice_ids = [
                        (4, invoice_id.id)]
                    # picking_id.purchase_id.invoice_id = invoice_id.id

                if picking_id.sale_id:
                    picking_id.sale_id.invoice_ids = [(4, invoice_id.id)]
                invoice_id.with_context(
                    check_move_validity=False)._onchange_partner_id()
                # invoice_id._onchange_invoice_line_ids()
                # invoice_id.with_context(
                #     check_move_validity=False)._recompute_tax_lines()

        elif not self.sh_separate_invoice:
            picking_partner_list = []

            for picking in active_ids:
                picking_id = self.env['stock.picking'].browse(picking)
                if picking_id.partner_id and picking_id.partner_id not in picking_partner_list:
                    picking_partner_list.append(picking_id.partner_id)
            for partner in picking_partner_list:
                # =====================================
                # Invoice Create
                # =====================================
                invoice_vals = {}
                picking_list = []
                invoice_vals = {
                    'partner_id': partner.id,
                    'user_id': self.env.user.id,
                    'invoice_date': self.sh_invoice_date,
                    'journal_id': self.sh_journal_id.id,
                }
                invoice_id = False
                if picking_id.picking_type_id.code == 'incoming' and self.sh_journal_id.type == 'purchase':
                    invoice_vals.update({'move_type': 'in_invoice'})
                    invoice_id = self.env['account.move'].sudo().with_context(
                        default_move_type='in_invoice').create(invoice_vals)
                if picking_id.picking_type_id.code == 'outgoing' and self.sh_journal_id.type == 'sale':
                    invoice_vals.update({'move_type': 'out_invoice'})
                    invoice_id = self.env['account.move'].sudo().with_context(
                        default_move_type='out_invoice').create(invoice_vals)
                # =====================================
                # Invoice Line Create
                # =====================================
                for picking in self.env['stock.picking'].search([('id', 'in', active_ids), ('invoice_done', '=', False), ('partner_id', '=', partner.id)]):
                    picking_list.append(picking.id)
                    for picking_line in picking.move_ids_without_package:
                        accounts = picking_line.product_id.product_tmpl_id.get_product_accounts(
                            invoice_id.fiscal_position_id)
                        if not accounts:
                            raise UserError(
                                _("No account defined for this product: " + picking_line.product_id.name))
                        invoice_line_vals = {}

                        if self.sh_journal_id.type == 'purchase':
                            invoice_line_vals = {
                                'product_id': picking_line.product_id.id,
                                'name': picking_line.product_id.name,
                                'quantity': picking_line.quantity,
                                'price_unit': picking_line.purchase_line_id.price_unit,
                                'tax_ids': [(6, 0, picking_line.purchase_line_id.taxes_id.ids)],
                                'move_id': invoice_id.id,
                                'account_id': accounts['expense'].id
                            }
                        elif self.sh_journal_id.type == 'sale':
                            invoice_line_vals = {
                                'product_id': picking_line.product_id.id,
                                'name': picking_line.product_id.name,
                                'quantity': picking_line.quantity,
                                'price_unit': picking_line.sale_line_id.price_unit,
                                'tax_ids': [(6, 0, picking_line.sale_line_id.tax_id.ids)],
                                'move_id': invoice_id.id,
                                'account_id': accounts['income'].id
                            }

                        invoice_line_id = self.env['account.move.line'].with_context(
                            check_move_validity=False).create(invoice_line_vals)
                        # =====================================
                        # Link with PO / sO
                        # =====================================
                        if picking_line.sale_line_id:
                            picking_line.sale_line_id.invoice_lines = [
                                (4, invoice_line_id.id)]

                        if picking_line.purchase_line_id:
                            picking_line.purchase_line_id.with_context(
                                check_move_validity=False).invoice_lines = [
                                (4, invoice_line_id.id)]

                    if picking.sale_id:
                        picking.sale_id.invoice_ids = [(4, invoice_id.id)]
                    if picking.purchase_id:
                        picking.purchase_id.invoice_ids = [
                            (4, invoice_id.id)]

                    #picking.invoice_done = True
                invoice_id.sh_picking_ids = [(6, 0, picking_list)]

                invoice_id.with_context(
                    check_move_validity=False)._onchange_partner_id()
                # invoice_id._onchange_invoice_line_ids()
                # invoice_id.with_context(
                #     check_move_validity=False)._recompute_tax_lines()
