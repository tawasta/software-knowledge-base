from odoo import fields, models


class Module(models.Model):

    _inherit = "software_knowledge_base.module"

    repository = fields.Many2one(
        comodel_name="software_knowledge_base.repository", string="Repository"
    )
