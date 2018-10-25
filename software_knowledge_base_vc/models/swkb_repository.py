# -*- coding: utf-8 -*-

# 1. Standard library imports:
import base64
import logging

# 2. Known third party imports:
import gitlab

# 3. Odoo imports (openerp):
from odoo import api, models
from odoo import _

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:
_logger = logging.getLogger()

class SWKBRepository(models.Model):
    # 1. Private attributes
    _inherit = 'software_knowledge_base.repository'

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    @api.multi
    def action_update_readme(self):
        for record in self:
            record._get_readme()

    # 8. Business methods
    @api.depends('url', 'vcs_host', 'vcs_team', 'master_branch')
    def _get_readme(self):
        for record in self:
            files = record.api_gitlab_get_files()

            record.readme = record.api_get_readme_from_repository_tree(files)

    # Gitlab
    def api_gitlab_get_session(self):
        self.ensure_one()

        host = self.vcs_host
        if not host:
            _logger.warning(_("No VCS host set: %s", self))
        session = gitlab.Gitlab(host.address,
                                token=host.api_token,
                                verify_ssl=host.api_verify_ssl)

        return session

    def api_gitlab_get_project(self):
        self.ensure_one()

        session = self.api_gitlab_get_session()

        project_path = "%s/%s" % (self.vcs_team.name, self.name)
        project = session.getproject(project_path)

        if not project:
            _logger.warning(_("No project found: %s" % self))
            return False

        return project

    def api_gitlab_get_files(self, *args, **kwargs):
        self.ensure_one()

        session = self.api_gitlab_get_session()
        project = self.api_gitlab_get_project()

        if not project:
            return False

        files = session.getrepositorytree(project['id'], *args, **kwargs)

        return files

    def api_gitlab_get_file(self, file_path):
        self.ensure_one()

        session = self.api_gitlab_get_session()
        project = self.api_gitlab_get_project()

        if not project:
            return False

        file = session.getfile(project['id'],
                               file_path,
                               project['default_branch'])

        return file

    def api_gitlab_get_readme(self):
        self.ensure_one()

        session = self.api_gitlab_get_session()
        project = self.api_gitlab_get_project()

        if not project:
            return False

        file = session.getfile(project['id'],
                               file['path'],
                               project['default_branch'])

        return file

    def api_get_readme_from_repository_tree(self, tree):
        if not tree:
            return False

        for file in tree:
            if file['name'][0:6].lower() == 'readme':
                readme_file = self.api_gitlab_get_file(file['path'])

                readme_file_content = base64.b64decode(readme_file['content'])

                return readme_file_content

        return False
