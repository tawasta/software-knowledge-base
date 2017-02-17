# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:
import gitlab

# 3. Odoo imports (openerp):
from openerp import api, fields, models
from openerp import _
from openerp.exceptions import ValidationError

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SWKBVcsHost(models.Model):
    # 1. Private attributes
    _inherit = 'software_knowledge_base.vcs_host'

    # 2. Fields declaration
    #readme = fields.Text(compute='_get_readme', store=True)
    vcs_api = fields.Many2one('software_knowledge_base.vcs_api', "VCS API")
    api_token = fields.Char("API token")
    api_verify_ssl = fields.Boolean("API verify SSL", default=True)

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    @api.multi
    def action_update_repositories(self):
        for record in self:
            record.validate_host()

            session = gitlab.Gitlab(record.address, token=record.api_token, verify_ssl=record.api_verify_ssl)

            for project in session.getall(session.getprojects):
                record.parse_repository_project(project)

    @api.multi
    def action_update_repository_readmes(self):
        for record in self:
            record.validate_host()

            for repository in record.repositories:
                repository.action_update_readme()

    # 8. Business methods
    def validate_host(self):
        for record in self:
            if not record.api_token:
                raise ValidationError(_("API token is not set"))
            if not record.vcs_api:
                raise ValidationError(_("VCS API is not set"))

    def parse_repository_project(self, project):
        self.ensure_one()

        api = self.vcs_api.code

        if api == 'github':
            # TODO: github api
            raise ValidationError(_("Github API is not implemented"))

        if api == 'gitlab':
            self.parse_repository_project_gitlab(project)

        if api == 'bitbucket':
            # TODO: bitbucket api
            raise ValidationError(_("Bitbucket API is not implemented"))

    def parse_repository_project_gitlab(self, project):
        repository_model = self.env['software_knowledge_base.repository']
        vcs_team_model = self.env['software_knowledge_base.vcs_team']

        # Check if team exists
        team_path = project['namespace']['path']
        vcs_team = vcs_team_model.search([('name', '=', team_path)])

        if not vcs_team:
            vcs_team = vcs_team_model.create({'name': team_path})

        repository = repository_model.search([('url', '=', project['web_url'])])

        if repository:
            # Update repository

            repository_values = {
                'name': project['name'],
                'master_branch': project['default_branch'],
                'vcs': 1,  # TODO
                'vcs_host': self.id,
                'vcs_team': vcs_team.id,
                'url': project['web_url'],
            }

            repository.write(repository_values)

        else:
            # Create new
            repository_values = {
                'name': project['name'],
                'url': project['web_url'],
                'master_branch': project['default_branch'],
                'vcs': 1,  # TODO
                'vcs_host': self.id,
                'vcs_team': vcs_team.id,
            }

            repository = repository_model.create(repository_values)

        return repository