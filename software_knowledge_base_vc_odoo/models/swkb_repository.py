# -*- coding: utf-8 -*-

# 1. Standard library imports:

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

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    @api.multi
    def action_update_odoo_modules(self):
        module_model = self.env['software_knowledge_base.module']

        for record in self:
            files = record.api_gitlab_get_files()

            if not files:
                continue

            for file in files:
                # Only parse directories
                if file['type'] == 'tree':
                    sub_files = record.api_gitlab_get_files(path=file['path'])

                    readme = record.api_get_readme_from_repository_tree(sub_files)

                    if readme:
                        if module_model.search([('name', '=', file['name'])]):
                            # Update module
                            module_model.write({
                                'readme': readme,
                                'repository': record.id,
                            })
                        else:
                            # Create a new module
                            module_model.create({
                                'name': file['name'],
                                'readme': readme,
                                'repository': record.id,
                            })


    # 8. Business methods

