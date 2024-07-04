from odoo import fields, models


class MarketingContactHistory(models.Model):
    _name = "marketing.contact.history"
    _description = "Marketing Message History"

    marketing_contact_id = fields.Many2one("whatsapp.messaging")
    phone = fields.Char(string="Whatsapp Number")
    contact_whatsapp_history_ids = fields.Many2many(
        "whatsapp.message", compute="_compute_contact_whatsapp_history_ids"
    )

    def _compute_contact_whatsapp_history_ids(self):
        for rec in self:
            where_query = self.env["whatsapp.message"]._where_calc(
                [("mobile_number", "=", rec.phone)]
            )
            from_clause, where_clause, where_clause_params = where_query.get_sql()
            select = "SELECT id from " + from_clause + " where " + where_clause + ";"
            self.env.cr.execute(select, where_clause_params)
            historys = self.env.cr.dictfetchall()
            history_ids = [x.get("id") for x in historys]
            rec.contact_whatsapp_history_ids = history_ids
