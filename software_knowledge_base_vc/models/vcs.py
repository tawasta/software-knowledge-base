from odoo import api, fields, models


class Vcs(models.Model):
    _name = "software_knowledge_base.vcs"
    _description = "Version Control System"
    _order = "name"

    name = fields.Char(string="Name", help="E.g. git or svn")

    description = fields.Text(string="Description", help="The full name")

    vcs_hosts = fields.One2many(
        comodel_name="software_knowledge_base.vcs_host",
        inverse_name="vcs",
        string="VCS Hosts",
        readme=True,
    )

    @api.one
    def name_get(self):
        display_name = "{} ({})".format(self.name, self.description)
        return (self.id, display_name)
