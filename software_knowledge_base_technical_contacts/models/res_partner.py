# -*- coding: utf-8 -*-
from odoo import models, fields


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
