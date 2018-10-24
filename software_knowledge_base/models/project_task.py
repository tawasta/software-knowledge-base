# -*- coding: utf-8 -*-
from odoo import models, fields


class ProjectTask(models.Model):

    _inherit = 'project.task'

    module_ids = fields.Many2many('software_knowledge_base.module', 'module_task_rel',  'task_id', 'module_id',
                                        string='Modules', help='Related modules')
