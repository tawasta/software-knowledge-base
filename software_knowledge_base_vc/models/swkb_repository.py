# -*- coding: utf-8 -*-

# 1. Standard library imports:
import base64

# 2. Known third party imports:
import gitlab

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SWKBRepository(models.Model):
    # 1. Private attributes
    _inherit = 'software_knowledge_base.repository'

    # 2. Fields declaration
    #readme = fields.Text(compute='_get_readme', store=True)

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
            host = record.vcs_host

            session = gitlab.Gitlab(host.address, token=host.api_token, verify_ssl=host.api_verify_ssl)
            project_path = "%s/%s" % (record.vcs_team.name, record.name)
            project = session.getproject(project_path)
            files = session.getrepositorytree(project['id'])

            for file in files:
                if file['path'][0:6].lower() == 'readme':
                    readme_file = session.getfile(project['id'], file['path'], project['default_branch'])

                    readme_file_content = base64.b64decode(readme_file['content'])

                    self.readme = readme_file_content
                    continue