# -*- coding: utf-8 -*-
# Part of Softhealer Technologies


from odoo import models, fields, api
from datetime import date, datetime


class MrpBackdateWizard(models.TransientModel):
    _name = 'sh.mrp.backdate.wizard'
    _description = "MRP Backdate Wizard"

    mrp_production_ids = fields.Many2many('mrp.production',)
    date_start = fields.Datetime(
        string="Scheduled Date", required=True, default=datetime.now())
    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.company)
    remarks = fields.Text(string="Remarks")
    is_remarks = fields.Boolean(
        related="company_id.remark_for_mrp_production", string="Is Remarks")
    is_remarks_mandatory = fields.Boolean(
        related="company_id.remark_mandatory_for_mrp_production", string="Is remarks mandatory")
    is_boolean = fields.Boolean()

    @api.onchange('date_start')
    def onchange_date_start(self):
        if str(self.date_start.date()) < str(date.today()):
           self.is_boolean = True
        else:
            self.is_boolean = False

    def open_mrp_backdate_wizard(self):
        active_ids = self.env.context.get('active_ids')


        return{
            'name': 'Assign Backdate',
            'res_model': 'sh.mrp.backdate.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('sh_all_in_one_backdate_adv.mrp_production_backdate_wizard_view_form').id,
            'context': {
                    'default_mrp_production_ids': [(6, 0, active_ids)],
            },
            'target': 'new',
            'type': 'ir.actions.act_window'
        }

    def assign_backdate(self):
        if self.company_id.enable_backdate_for_mrp:

            for mrp_production in self.mrp_production_ids:
                if mrp_production.workorder_ids:
                    mrp_production.workorder_ids[0].write({
                        'date_start' : self.date_start,
                    })

                stock_moves = self.env['stock.move'].search(['|','|','|',('production_id','=',mrp_production.id),('created_production_id','=',mrp_production.id),('raw_material_production_id','=',mrp_production.id),('origin','=',mrp_production.name)])

                product_moves = self.env['stock.move.line'].search([('move_id','in',stock_moves.ids)])

                account_moves = self.env['account.move'].search([('stock_move_id','in',stock_moves.ids)])

                valuation_layers = self.env['stock.valuation.layer'].search([('stock_move_id','in',stock_moves.ids)])

                for account_move in account_moves:
                    account_move.button_draft()
                    account_move.name = False
                    account_move.date = self.date_start
                    account_move.action_post()

                for move in stock_moves:
                    move.date = self.date_start
                    move.remarks_for_mrp = self.remarks if self.remarks else ''

                for move in product_moves:
                    move.date = self.date_start

                for layer in valuation_layers:
                    self.env.cr.execute("""
                        Update stock_valuation_layer set create_date='%s' where id=%s; 
                    """ %(self.date_start, layer.id))

                mrp_production.with_context(force_date=True).write({
                    'date_start':self.date_start,
                    'remarks':self.remarks if self.remarks else ''
                })
