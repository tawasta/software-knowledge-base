from odoo import fields, models


class SWKBInstallationClassification(models.Model):
    _name = "software_knowledge_base.installation.classification"
    _description = "Installation classifications"

    name = fields.Char(
        string="Classification name", help="Name for this classification"
    )
