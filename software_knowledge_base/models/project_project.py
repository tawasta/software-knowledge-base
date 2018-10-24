# -*- coding: utf-8 -*-
from odoo import osv, fields, models


class ProjectProject(models.Model):

    _inherit = 'project.project'

    installation_ids = fields.Many2many(
        comodel_name='software_knowledge_base.installation',
        relation='installation_project_rel',
        column1='project_id',
        column2='installation_id',
        string='Installations',
        help='Installations related to this project.'
    )
