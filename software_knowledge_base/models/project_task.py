from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    module_ids = fields.Many2many(
        comodel_name="software_knowledge_base.module",
        relation="module_task_rel",
        column1="task_id",
        column2="module_id",
        string="Modules",
        help="Related modules",
    )
