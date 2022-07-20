from odoo import _, fields, models
from odoo.exceptions import ValidationError


class VcsHost(models.Model):
    _name = "software_knowledge_base.vcs_host"
    _description = "Version Control System Host"
    _order = "name"

    name = fields.Char(string="Name", help="E.g. github or bitbucket", required=True)

    vcs_id = fields.Many2one(
        comodel_name="software_knowledge_base.vcs", string="VCS", required=True
    )

    repository_ids = fields.One2many(
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

    vcs_api_id = fields.Many2one("software_knowledge_base.vcs_api", "VCS API")
    api_token = fields.Char("API token")

    # provider = fields.Many2one('software_knowledge_base.vcs_provider', string='Provider')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "{} ({})".format(self.name, self.address)))

        return result

    def action_update_repositories(self):
        for record in self:
            api_code = record.vcs_api_id.code
            method_name = f"{api_code}_update_repositories"
            if hasattr(self, method_name):
                getattr(record, method_name)()

    def validate_host(self):
        for record in self:
            if not record.api_token:
                raise ValidationError(_("API token is not set"))
            if not record.vcs_api:
                raise ValidationError(_("VCS API is not set"))
