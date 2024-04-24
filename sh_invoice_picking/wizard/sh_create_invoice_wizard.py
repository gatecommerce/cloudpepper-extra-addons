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
    sh_separate_invoice = fields.Boolean(string="Separate Invoice ?")
    journal_ids = fields.Many2many('account.journal', string="Journals")

    def action_create_invoices(self):
        active_ids = self.env.context.get('active_ids')
        
        # Code for inside picking form create invoice
        
        
        picking_ids = self.env['stock.picking'].browse(active_ids)
        if picking_ids:
            moves = False
            if len(active_ids) == 1 or self.sh_separate_invoice:
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
                                'invoice_date': self.sh_invoice_date,
                            })
                            
                            if move.invoice_line_ids and move.sh_picking_ids:
                                for picking_id in move.sh_picking_ids:
                                    picking_product_ids = []
                                    picking_product_ids = move.sh_picking_ids.move_ids_without_package.mapped('product_id')
                                    remove_lines = move.invoice_line_ids.filtered(lambda m:m.product_id.id not in picking_product_ids.ids)
                                    if remove_lines:
                                        remove_lines.unlink()
            else:
                for picking in picking_ids:
                    if picking.state == 'cancel':
                        continue
                    
                    if picking.picking_type_id.code == 'incoming' and picking.purchase_id and self.sh_journal_id.type == 'purchase':
                        self.auto_validate_picking(picking)
                        draft_bills = picking.purchase_id.invoice_ids.filtered(lambda x:x.state == 'draft' and x.move_type == 'in_invoice')
                        
                        if picking.purchase_id.invoice_ids and draft_bills:
                            bill_exist = False
                            existing_bill = False
                            for bill in draft_bills:
                                if bill.sh_picking_ids:
                                    for bill_picking in bill.sh_picking_ids:
                                        if bill_picking.id in picking_ids.ids:
                                            bill_exist = True
                                            existing_bill = bill
                                            break
                                    
                            if bill_exist:
                                for move_line in picking.move_ids_without_package:
                                    if move_line.product_id.id in existing_bill.invoice_line_ids.mapped('product_id').ids:
                                        inv_line = bill.invoice_line_ids.filtered(lambda x:x.product_id.id == move_line.product_id.id)
                                        purchase_line_id = picking.purchase_id.order_line.filtered(lambda x:x.product_id.id == move_line.product_id.id)
                                        if purchase_line_id and len(purchase_line_id) > 1:
                                            purchase_line_id = purchase_line_id[0]
                                        inv_line.write({'quantity':inv_line.quantity + move_line.quantity,'purchase_line_id' : purchase_line_id.id,})
                                        
                                    else:
                                        purchase_line = picking.purchase_id.order_line.filtered(lambda x:x.product_id.id == move_line.product_id.id)
                                        if purchase_line and len(purchase_line) > 1:
                                            purchase_line = purchase_line[0]
                                        inv_line_id = self.env['account.move.line'].sudo().create({
                                            'product_id' : move_line.product_id.id,
                                            'name': picking.purchase_id.name + " : " + purchase_line.name,
                                            'quantity' : move_line.quantity,
                                            'price_unit' : purchase_line.price_unit,
                                            'tax_ids' : purchase_line.taxes_id.ids,
                                            'move_id' : existing_bill.id,
                                            'purchase_line_id' : purchase_line.id,
                                        })
                                        
                                existing_bill.write({
                                    'sh_picking_ids': [(4, picking.id)],
                                    'journal_id': self.sh_journal_id.id,
                                })
                            else:
                                self.create_vendor_bill(picking)
                        else:
                            self.create_vendor_bill(picking)
                                
                    elif picking.picking_type_id.code == 'outgoing' and picking.sale_id and self.sh_journal_id.type == 'sale':
                        self.auto_validate_picking(picking)

                        draft_invoices = picking.sale_id.invoice_ids.filtered(lambda x:x.state == 'draft' and x.move_type == 'out_invoice')
                        
                        if picking.sale_id.invoice_ids and draft_invoices:
                            invoice_exist = False
                            existing_invoice = False
                            for inv_id in draft_invoices:
                                if inv_id.sh_picking_ids:
                                    for invoice_picking in inv_id.sh_picking_ids:
                                        if invoice_picking.id in picking_ids.ids:
                                            invoice_exist = True
                                            existing_invoice = inv_id
                                            break
                                    
                            if invoice_exist:
                                for move_line in picking.move_ids_without_package:
                                    if move_line.product_id.id in existing_invoice.invoice_line_ids.mapped('product_id').ids:
                                        inv_line = inv_id.invoice_line_ids.filtered(lambda x:x.product_id.id == move_line.product_id.id)
                                        if inv_line and len(inv_line) > 1:
                                            inv_line = inv_line[0]
                                        inv_line.write({'quantity':inv_line.quantity + move_line.quantity})
                                    else:
                                        sale_line = picking.sale_id.order_line.filtered(lambda x:x.product_id.id == move_line.product_id.id)
                                        if sale_line and len(sale_line) > 1:
                                            sale_line = sale_line[0]
                                        inv_line = self.env['account.move.line'].sudo().create({
                                            'product_id' : move_line.product_id.id,
                                            'name': picking.sale_id.name + " : " + sale_line.name,
                                            'quantity' : move_line.quantity,
                                            'price_unit' : sale_line.price_unit,
                                            'tax_ids' : sale_line.tax_id.ids,
                                            'move_id' : existing_invoice.id,
                                        })
                                        sale_line.write({'invoice_lines': [(4, inv_line.id)]})
                                existing_invoice.write({
                                    'sh_picking_ids': [(4, picking.id)],
                                    'journal_id': self.sh_journal_id.id,
                                })
                            else:
                                self.create_customer_invoice(picking)
                        else:
                            self.create_customer_invoice(picking)
                    else:
                        return


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

    def create_vendor_bill(self,picking):
        '''Creates new vendor bill'''
        bill_vals = {
            'partner_id' : picking.partner_id.id,
            'move_type' : 'in_invoice',
            'sh_picking_ids': [(4, picking.id)],
            'journal_id': self.sh_journal_id.id,
            'invoice_date': self.sh_invoice_date,
        }
        bill_id = self.env['account.move'].sudo().create(bill_vals)
        if bill_id:
            invoice_lines = []
            for move_line in picking.move_ids_without_package:
                purchase_line = picking.purchase_id.order_line.filtered(lambda x:x.product_id.id == move_line.product_id.id)
                if purchase_line and len(purchase_line) > 1:
                    purchase_line = purchase_line[0]
                invoice_lines.append((0,0,{
                    'product_id' : move_line.product_id.id or False,
                    'name': picking.purchase_id.name + " : " + purchase_line.name,
                    'quantity' : move_line.quantity,
                    'price_unit' : purchase_line.price_unit,
                    'tax_ids' : purchase_line.taxes_id.ids,
                    'purchase_line_id' : purchase_line.id,
                }))
            bill_id.write({'invoice_line_ids': invoice_lines})
            picking.purchase_id.write({'invoice_ids' : [(4, bill_id.id)]})

        return bill_id or False
        
    def create_customer_invoice(self,picking):
        '''Creates new customer invoice'''
        invoice_vals = {
            'partner_id' : picking.partner_id.id,
            'move_type' : 'out_invoice',
            'sh_picking_ids': [(4, picking.id)],
            'journal_id': self.sh_journal_id.id,
            'invoice_date': self.sh_invoice_date,
        }
        invoice_id = self.env['account.move'].sudo().create(invoice_vals)
        if invoice_id:
            invoice_lines = []
            for move_line in picking.move_ids_without_package:
                sale_line = picking.sale_id.order_line.filtered(lambda x:x.product_id.id == move_line.product_id.id)
                if sale_line and len(sale_line) > 1:
                    sale_line = sale_line[0]
                invoice_lines.append((0,0,{
                    'product_id' : move_line.product_id.id or False,
                    'name': picking.sale_id.name + " : " + sale_line.name,
                    'quantity' : move_line.quantity,
                    'price_unit' : sale_line.price_unit,
                    'tax_ids' : sale_line.tax_id.ids,
                }))
            invoice_id.write({'invoice_line_ids': invoice_lines})
            picking.sale_id.write({'invoice_ids' : [(4, invoice_id.id)]})
            
            for line in invoice_id.invoice_line_ids:
                sale_line_id = picking.sale_id.order_line.filtered(lambda x:x.product_id.id == line.product_id.id)
                if sale_line_id:
                    sale_line_id.write({'invoice_lines' : [(4, line.id)]})
            
        return invoice_id or False
        