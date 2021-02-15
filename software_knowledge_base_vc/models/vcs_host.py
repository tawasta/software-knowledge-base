import gitlab

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class VcsHost(models.Model):
    _name = "software_knowledge_base.vcs_host"
    _description = "Version Control System Host"
    _order = "name"

    name = fields.Char(string="Name", help="E.g. github or bitbucket")

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
    api_verify_ssl = fields.Boolean("API verify SSL", default=True)

    # provider = fields.Many2one('software_knowledge_base.vcs_provider', string='Provider')

    @api.one
    def name_get(self):
        display_name = "{} ({})".format(self.name, self.address)
        return (self.id, display_name)

    @api.multi
    def action_update_repositories(self):
        for record in self:
            record.validate_host()

            session = gitlab.Gitlab(
                record.address, token=record.api_token, verify_ssl=record.api_verify_ssl
            )

            for project in session.getall(session.getprojects):
                record.parse_repository_project(project)

    @api.multi
    def action_update_repository_readmes(self):
        for record in self:
            record.validate_host()

            for repository in record.repositories:
                repository.action_update_readme()

    def validate_host(self):
        for record in self:
            if not record.api_token:
                raise ValidationError(_("API token is not set"))
            if not record.vcs_api:
                raise ValidationError(_("VCS API is not set"))

    def parse_repository_project(self, project):
        self.ensure_one()

        api = self.vcs_api.code

        if api == "github":
            # TODO: github api
            raise ValidationError(_("Github API is not implemented"))

        if api == "gitlab":
            self.parse_repository_project_gitlab(project)

        if api == "bitbucket":
            # TODO: bitbucket api
            raise ValidationError(_("Bitbucket API is not implemented"))

    def parse_repository_project_gitlab(self, project):
        repository_model = self.env["software_knowledge_base.repository"]
        vcs_team_model = self.env["software_knowledge_base.vcs_team"]

        # Check if team exists
        team_path = project["namespace"]["path"]
        vcs_team = vcs_team_model.search([("name", "=", team_path)])

        if not vcs_team:
            vcs_team = vcs_team_model.create({"name": team_path})

        repository = repository_model.search([("url", "=", project["web_url"])])

        if repository:
            # Update repository
            repository_values = {
                "name": project["name"],
                "master_branch": project["default_branch"],
                "vcs": 1,  # TODO
                "vcs_host": self.id,
                "vcs_team": vcs_team.id,
                "url": project["web_url"],
            }

            repository.write(repository_values)

        else:
            # Create a new
            repository_values = {
                "name": project["name"],
                "url": project["web_url"],
                "master_branch": project["default_branch"],
                "vcs": 1,  # TODO
                "vcs_host": self.id,
                "vcs_team": vcs_team.id,
            }

            repository = repository_model.create(repository_values)

        return repository
