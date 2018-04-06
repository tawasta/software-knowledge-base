# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SWKBInstallationPoll(models.Model):
    # 1. Private attributes
    _name = 'software_knowledge_base.installation_poll'
    _order = 'id DESC'

    # 2. Fields declaration
    installation_id = fields.Many2one(
        comodel_name='software_knowledge_base.installation',
    )

    name = fields.Char(
        string='Url',
    )

    description = fields.Char(
        string='Description'
    )

    delay = fields.Float(
        string='Delay in seconds',
    )

    success = fields.Boolean(
        string='Success',
        default=False,
    )

    # 3. Default methods

    # 4. Compute and search fields

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
