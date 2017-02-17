# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:
import gitlab

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SWKBVcsHost(models.Model):
    # 1. Private attributes
    _inherit = 'software_knowledge_base.vcs_host'

    # 2. Fields declaration
    #readme = fields.Text(compute='_get_readme', store=True)
    readme_autofetch = fields.Boolean("Automatically fetch README files")
    api_token = fields.Char("API token")
    verify_ssl = fields.Boolean("Verify SSL", default=True)

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    @api.multi
    def action_update_repositories(self):
        for record in self:
            if not record.api_token:
                return False

            session = gitlab.Gitlab(record.address, token=record.api_token, verify_ssl=record.verify_ssl)

            for project in session.getall(session.getprojects):
                record.parse_repository_project(project)

    # 8. Business methods
    def parse_repository_project(self, project):
        self.ensure_one()

        repository_model = self.env['software_knowledge_base.repository']

        if repository_model.search([('url', '=', project['http_url_to_repo'])]):
            # Update repository
            repository_values = {
                'name': project['name'],
                'master_branch': project['default_branch'],
                'vcs': 1,  # TODO
                'vcs_host': self.id,
            }

            repository_model.write(repository_values)

        else:
            # Create new
            repository_values = {
                'name': project['name'],
                'url': project['http_url_to_repo'],
                'master_branch': project['default_branch'],
                'vcs': 1,  # TODO
                'vcs_host': self.id,
            }

            repository_model.create(repository_values)
