# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Installation(models.Model):

    _inherit = 'software_knowledge_base.installation'

    technical_contact_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='installation_techcontact_rel',
        column1='instalation_id',
        column2='partner_id',
        string='Technical contacts',
        help='Technical contacts for this installation',
        domain=[('is_company', '=', False)]
    )

    technical_contact_emails = fields.Char(
        string="Technical contact emails",
        compute='compute_technical_contact_emails'
    )

    @api.multi
    def compute_technical_contact_emails(self):
        # Technical contacts in a copy-ready string
        for record in self:
            emails = filter(None, record.technical_contact_ids.mapped('email'))
            record.technical_contact_emails = ", ".join(emails)
