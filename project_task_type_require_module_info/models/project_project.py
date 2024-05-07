from odoo import fields, models


class Project(models.Model):

    _inherit = "project.project"

    module_info_required_stage_ids = fields.Many2many(
        comodel_name="project.task.type",
        string="Task Stages Requiring Module Info",
    )
