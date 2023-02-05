from odoo import fields, models


class Platform(models.Model):
    _name = "software_knowledge_base.platform"
    _description = "Platform"
    _inherit = ["mail.thread"]
    _order = "name"

    name = fields.Char(string="Name", help="E.g. Odoo 14 or Drupal 9")
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True)
    image = fields.Image(
        string="Platform icon",
        readonly=False,
        max_width=256,
        max_height=256,
    )

    installation_ids = fields.One2many(
        string="Installations",
        comodel_name="software_knowledge_base.installation",
        inverse_name="platform_id",
    )
