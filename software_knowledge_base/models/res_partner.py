# -*- coding: utf-8 -*-
from odoo import models, fields


class ResPartner(models.Model):

    _inherit = 'res.partner'

    # Note the misnamed table module_partner_rel!
    installation_ids = fields.Many2many('software_knowledge_base.installation', 'module_partner_rel', 'partner_id', 'installation_id',
                                                 string='Installations')
