from odoo import fields, models


class SWKBExternalComponent(models.Model):
    _name = "software_knowledge_base.external_component"
    _description = "External component"
    _inherit = ["mail.thread"]
    _order = "name"

    name = fields.Char(string="Name")

    url = fields.Char(string="Homepage")
    features = fields.Text(string="Features")

    installation_ids = fields.Many2many(
        comodel_name="software_knowledge_base.installation",
        relation="installation_ext_comp_rel",
        column1="ext_comp_id",
        column2="installation_id",
        string="Installations",
        help="Installations using this component.",
    )

    installation_notes = fields.Text(string="Installation notes")

    additional_info = fields.Text(
        string="Additional info", help="Additional information"
    )
