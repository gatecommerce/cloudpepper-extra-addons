# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from ast import literal_eval

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
            
            picking_ids = self.env['stock.picking'].browse(active_ids)
            if picking_ids:
                for picking in picking_ids:
                    if picking.picking_type_id.code != first_type:
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
    # sh_separate_invoice = fields.Boolean(string="Separate Invoice ?")
    journal_ids = fields.Many2many('account.journal', string="Journals")

    def action_create_invoices(self):
        active_ids = self.env.context.get('active_ids')
        
        # Code for inside picking form create invoice
        # if len(active_ids) == 1 or self.sh_separate_invoice:
        
        picking_ids = self.env['stock.picking'].browse(active_ids)
        if picking_ids:
            for picking in picking_ids:
                if picking.state == 'cancel':
                    continue

                account_move_obj = self.env['account.move']
                if picking.picking_type_id.code == 'incoming' and picking.purchase_id and self.sh_journal_id.type == 'purchase':
                    self.auto_validate_picking(picking)
                    result = picking.purchase_id.action_create_invoice()
                    if result and result.get('domain'):
                        domain= literal_eval(result.get('domain'))
                        if result.get('res_id'):
                            domain.append(('id', '=', result.get('res_id')))
                        moves = account_move_obj.search(domain)
                elif picking.picking_type_id.code == 'outgoing' and picking.sale_id and self.sh_journal_id.type == 'sale':
                    self.auto_validate_picking(picking)
                    moves = picking.sale_id._create_invoices(True, True)
                else:
                    return
                if moves:
                    for move in moves:
                        move.write({
                            'sh_picking_ids': [(4, picking.id)],
                            'journal_id': self.sh_journal_id.id,
                        })
                        
                        if move.invoice_line_ids and move.sh_picking_ids:
                            for picking_id in move.sh_picking_ids:
                                picking_product_ids = []
                                picking_product_ids = move.sh_picking_ids.move_ids_without_package.mapped('product_id')
                                remove_lines = move.invoice_line_ids.filtered(lambda m:m.product_id.id not in picking_product_ids.ids)
                                if remove_lines:
                                    remove_lines.unlink()

    def auto_validate_picking(self, picking):
        if picking.state != 'done':
            for move in picking.move_ids_without_package:
                move.sudo().write({
                    'quantity': move.product_uom_qty,
                })

            if picking.state in ['draft']:
                picking.action_confirm()
            if picking.state in ['confirmed']:
                picking.action_assign()
            if picking.state in ['assigned']:
                picking.with_context(force_validate=True).button_validate()
