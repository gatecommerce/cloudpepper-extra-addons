# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
SCOPE = 'sh_login'


class LoginUserWizard(models.TransientModel):
    _name = 'login.other.wizard'
    _description = "Used to Login From Other User"
    sh_user_id = fields.Many2one("res.users", string="Login As")
    sh_group_ids = fields.Many2many(
        "res.groups", related="sh_user_id.groups_id", string="Groups")

    def action_do_login(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/sh_login?uid=%s' % self.sh_user_id.id,
            'target': 'self',
        }
