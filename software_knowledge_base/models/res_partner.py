# -*- coding: utf-8 -*-
from odoo import models, fields


class ResPartner(models.Model):

    _inherit = 'res.partner'

    # Note the misnamed table module_partner_rel!
    installation_ids = fields.Many2many(
        comodel_name='software_knowledge_base.installation',
        relation='module_partner_rel',
        column1='partner_id',
        column2='installation_id',
        string='Installations'
    )
