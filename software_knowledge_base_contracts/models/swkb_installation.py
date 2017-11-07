# -*- coding: utf-8 -*-
from openerp import api, fields, models


class SWKBInstallation(models.Model):

    _inherit = 'software_knowledge_base.installation'

    account_analytic_account_id = fields.Many2one(
        string='Contract',
        comodel_name='account.analytic.account',
        domain=[('type', '=', 'contract')],
    )
    analytic_account_invoice_line_ids = fields.One2many(
        string='Contract line',
        comodel_name='account.analytic.invoice.line',
        inverse_name='installation_id',
    )

