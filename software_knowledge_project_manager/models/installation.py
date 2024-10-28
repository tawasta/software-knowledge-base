from odoo import fields, models


class Installation(models.Model):

    _inherit = "software_knowledge_base.installation"

    project_manager_id = fields.Many2one(
        string="Project Manager (Owner)",
        comodel_name="res.users",
        tracking=True,
    )
