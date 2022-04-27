import logging
from odoo import fields, models

_logger = logging.getLogger()


class SWKBRepository(models.Model):

    _name = "software_knowledge_base.repository"
    _description = "Repository"
    _inherit = ["mail.thread"]
    _order = "name"

    name = fields.Char(
        string="Name", help='E.g. "odoo-customizations" or "moodle-extension"'
    )
    description = fields.Text(string="Description")

    readme = fields.Text(string="Readme")

    active = fields.Boolean(default=True)

    url = fields.Char(string="URL", help="The full URL")

    url_readonly = fields.Char(
        string="URL", help="The full URL", readonly=True, store=True
    )

    vcs = fields.Many2one(
        comodel_name="software_knowledge_base.vcs",
        string="Type",
    )

    vcs_host = fields.Many2one(
        comodel_name="software_knowledge_base.vcs_host",
        string="Host",
    )

    vcs_team = fields.Many2one(
        comodel_name="software_knowledge_base.vcs_team", string="Team"
    )

    tag_ids = fields.Many2many(
        comodel_name="software_knowledge_base.repository_tag",
        relation="software_knowledge_base_repository_tag_rel",
        column1="id",
        column2="repository_id",
        string="Tags",
    )

    default_branch = fields.Char(string="Default branch", default="main")
