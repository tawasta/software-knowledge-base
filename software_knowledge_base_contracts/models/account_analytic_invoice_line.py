# -*- coding: utf-8 -*-
from openerp import api, fields, models


class AccountAnalyticInvoiceLine(models.Model):

    _inherit = 'account.analytic.invoice.line'

    installation_id = fields.Many2one(
        string='Installation',
        comodel_name='software_knowledge_base.installation',
    )

    @api.multi
    def write(self, values):
        res = super(AccountAnalyticInvoiceLine, self).write(values)

        if 'installation_id' in values:
            for record in self:
                if record.installation_id:
                    record.installation_id.account_analytic_account_id = record.analytic_account_id.id

        return res