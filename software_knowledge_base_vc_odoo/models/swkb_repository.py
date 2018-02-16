# -*- coding: utf-8 -*-

# 1. Standard library imports:
import base64
import re

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


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
    def action_update_odoo_modules(self):
        SWKBModule = self.env['software_knowledge_base.module']

        for record in self:
            files = record.api_gitlab_get_files()

            if not files:
                continue

            for file in files:
                # Only parse directories
                if file['type'] == 'tree':
                    sub_files = record.api_gitlab_get_files(path=file['path'])

                    readme = record.api_get_readme_from_repository_tree(sub_files)
                    manifest = record.api_get_manifest_from_repository_tree(sub_files)
                    summary = ''

                    if manifest:
                        pattern = "['\"](name|summary|version)[\"'][:][ ]['\"](.*)['\"]"
                        p = re.compile(pattern)

                        result = dict(p.findall(manifest))

                        if 'summary' in result:
                            summary = result['summary']

                    existing_module = SWKBModule.search([
                        ('name', '=', file['name']),
                        ('repository', '=', record.id),
                    ])

                    if existing_module:
                        # Update module
                        existing_module.write({
                            'readme': readme,
                            'repository': record.id,
                            'summary': summary,
                        })
                    else:
                        # Create a new module
                        SWKBModule.create({
                            'name': file['name'],
                            'readme': readme,
                            'repository': record.id,
                            'summary': summary,
                        })

    # 8. Business methods
    def api_get_manifest_from_repository_tree(self, tree):
        if not tree:
            return False

        for file in tree:
            if file['name'][0:15].lower() == '__manifest__.py' or \
                file['name'][0:14] == '__openerp__.py':
                manifest_file = self.api_gitlab_get_file(file['path'])
                manifest_file_content = base64.b64decode(manifest_file['content'])

                return manifest_file_content

        return False
