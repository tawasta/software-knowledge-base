from odoo import fields, models


class Installation(models.Model):
    _inherit = "software_knowledge_base.module"

    module_guide = fields.Char(
        string="Module guide URL",
    )
