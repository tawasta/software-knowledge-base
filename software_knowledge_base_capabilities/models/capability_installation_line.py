from odoo import fields, models

class CapabilityInstallationLine(models.Model):
    _name = "swkb.capability.installation.line"
    _description = "Capability linked to an Installation"
    _order = "id"

    installation_id = fields.Many2one(
        "software_knowledge_base.installation",
        required=True,
        ondelete="cascade",
        index=True,
    )
    capability_id = fields.Many2one(
        "swkb.capability",
        required=True,
        index=True,
    )
    status = fields.Selection(
        [
            ("not_installed", "ei asennettu"),
            ("installed", "asennettu"),
        ],
        default="not_installed",
        string="Status",
        help="Onko tämän capabilityn moduulit asennettu tähän asennukseen.",
    )
