from odoo import fields, models


class Platform(models.Model):
    _name = "software_knowledge_base.platform"
    _description = "Platform"
    _inherit = ["mail.thread"]
    _order = "name"

    name = fields.Char(string="Name", help="E.g. Odoo 10 or Drupal 8")

    description = fields.Text(string="Description")

    active = fields.Boolean(default=True)
