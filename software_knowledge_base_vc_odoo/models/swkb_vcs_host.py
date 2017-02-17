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

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    @api.multi
    def action_update_odoo_modules(self):
        for record in self:
            for repository in record.repositories:
                repository.action_update_odoo_modules()


    # 8. Business methods
