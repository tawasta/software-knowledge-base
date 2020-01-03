# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResPartner(models.Model):

    _inherit = 'res.partner'

    installation_technical_contact_ids = fields.Many2many(
        comodel_name='software_knowledge_base.installation',
        relation='installation_techcontact_rel',
        column1='partner_id',
        column2='instalation_id',
        string='Installations (Technical contact)',
        help='Installations where the partner has been marked as a '
             'technical contact.'
    )

    server_technical_contact_ids = fields.Many2many(
        comodel_name='software_knowledge_base.server',
        string='Servers (Technical contact)',
        compute='_compute_server_technical_contact_ids',
    )

    def _compute_server_technical_contact_ids(self):
        for record in self:
            record.server_technical_contact_ids = \
                record.installation_technical_contact_ids.mapped('server_id')
