from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # Note the misnamed table module_partner_rel!
    installation_ids = fields.Many2many(
        comodel_name="software_knowledge_base.installation",
        relation="module_partner_rel",
        column1="partner_id",
        column2="installation_id",
        string="Installations",
        domain=[("state", "=", "ready")],
    )

    installation_technical_contact_ids = fields.Many2many(
        comodel_name="software_knowledge_base.installation",
        relation="installation_techcontact_rel",
        column1="partner_id",
        column2="instalation_id",
        string="Installations (Technical contact)",
        domain=[("state", "=", "ready")],
        help="Installations where the partner has been marked as a "
        "technical contact.",
    )
