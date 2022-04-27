from odoo import fields, models
from odoo import _
from odoo.exceptions import ValidationError


class VcsHost(models.Model):
    _name = "software_knowledge_base.vcs_host"
    _description = "Version Control System Host"
    _order = "name"

    name = fields.Char(string="Name", help="E.g. github or bitbucket", required=True)

    vcs = fields.Many2one(
        comodel_name="software_knowledge_base.vcs", string="VCS", required=True
    )

    repositories = fields.One2many(
        comodel_name="software_knowledge_base.repository",
        inverse_name="vcs_host",
        string="Repositories",
        readonly=True,
    )

    description = fields.Text(
        string="Description", help="Longer description, if needed"
    )

    address = fields.Char(
        string="Address", help="E.g. https://github.com or 192.168.100.100"
    )

    address_readme = fields.Char(
        string="Readme Address", help="E.g. https://raw.githubusercontent.com"
    )

    vcs_api = fields.Many2one("software_knowledge_base.vcs_api", "VCS API")
    api_token = fields.Char("API token")

    # provider = fields.Many2one('software_knowledge_base.vcs_provider', string='Provider')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "{} ({})".format(self.name, self.address)))

        return result

    def action_update_repositories(self):
        for record in self:
            # TODO
            pass

    def validate_host(self):
        for record in self:
            if not record.api_token:
                raise ValidationError(_("API token is not set"))
            if not record.vcs_api:
                raise ValidationError(_("VCS API is not set"))
