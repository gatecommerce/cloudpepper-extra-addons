# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields,_


class ShStockPicking(models.Model):
    _inherit = 'stock.picking'

    sh_invoice_count = fields.Integer('Invoices', compute='_compute_invoices_count',search='_search_count')
    invoice_done = fields.Boolean("Invoice Done", default=False)

    def _search_count(self, operator, value):

        results = []
        moves = self.env['account.move'].search([])
        if operator == '>':
            for rec in moves:
                picking = self.env['stock.picking'].search([('id','in',rec.sh_picking_ids.ids)])
                if picking:
                    results.extend(picking.ids)

            return [('id', 'in', results)]
        elif operator == '=':

            picking = self.env['stock.picking'].search([('id','not in',moves.mapped('sh_picking_ids').ids)])
            if picking:
                results.extend(picking.ids)

            return [('id', 'in', results)]

    def _compute_invoices_count(self):
        if self:
            self.sh_invoice_count = 0
            for rec in self:
                if rec.picking_type_id.code == 'outgoing':
                    move_type = 'out_invoice'
                elif rec.picking_type_id.code == 'incoming':
                    move_type = 'in_invoice'
                invoice_ids = len(self.env['account.move'].sudo().search(
                    [('sh_picking_ids', 'in', rec.id), ('move_type', '=', move_type)]).ids)
                if invoice_ids:
                    rec.sh_invoice_count = invoice_ids

    def action_invoices(self):
        if self:
            if self.picking_type_id.code == 'outgoing':
                invoices = self.env['account.move'].sudo().search(
                    [('sh_picking_ids', 'in', self.ids), ('move_type', '=', 'out_invoice')])
                action = self.env.ref(
                    'account.action_move_in_invoice_type').sudo().read()[0]
                if len(invoices) > 1:
                    action['domain'] = [
                        ('sh_picking_ids', 'in', self.ids), ('move_type', '=', 'out_invoice')]
                elif len(invoices) == 1:
                    action['views'] = [
                        (self.env.ref('account.view_move_form').id, 'form')]
                    action['res_id'] = invoices.ids[0]
                else:
                    action = {'type': 'ir.actions.act_window_close'}
                return action
            elif self.picking_type_id.code == 'incoming':
                invoices = self.env['account.move'].sudo().search(
                    [('sh_picking_ids', 'in', self.ids), ('move_type', '=', 'in_invoice')])
                action = self.env.ref(
                    'account.action_move_in_invoice_type').read()[0]
                if len(invoices) > 1:
                    action['domain'] = [
                        ('sh_picking_ids', 'in', self.ids), ('move_type', '=', 'in_invoice')]
                elif len(invoices) == 1:
                    action['views'] = [
                        (self.env.ref('account.view_move_form').id, 'form')]
                    action['res_id'] = invoices.ids[0]
                else:
                    action = {'type': 'ir.actions.act_window_close'}
                return action

    def action_create_invoice(self):

        context = {'default_stock_picking_id': self.id}
        if self.sh_invoice_count > 0:
            context['invoice_already_created'] = 'haa_ji'

        return {
            'name': 'Create Invoice',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'sh.create.invoice.wizard',
            'context': context,
            'target': 'new',
        }
