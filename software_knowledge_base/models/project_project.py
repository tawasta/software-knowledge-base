# -*- coding: utf-8 -*-
from odoo import osv, fields, models


class ProjectProject(models.Model):

    _inherit = 'project.project'

    installation_ids = fields.Many2many('software_knowledge_base.installation', 'installation_project_rel', 'project_id', 'installation_id',
                                                 string='Installations', help='Installations related to this project.')
