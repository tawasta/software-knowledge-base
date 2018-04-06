# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models


# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SWKBOperatingSystem(models.Model):
    # 1. Private attributes
    _name = 'software_knowledge_base.operating_system'
    _description = 'Operating system'
    _order = 'name'

    # 2. Fields declaration
    display_name = fields.Char(
        string='Display name',
        compute='_compute_display_name',
    )

    server_ids = fields.One2many(
        comodel_name='software_knowledge_base.server',
        inverse_name='operating_system_id',
        string='Servers'
    )

    name = fields.Char(
        string='Name',
        help='E.g. "Debian" or "CentOS"',
    )

    active = fields.Boolean(
        string='Active',
        default=True,
    )

    version = fields.Char(
        string='Version',
    )

    codename = fields.Char(
        string='Codename',
        help='E.g. "Buster" or "Zapus"',
    )

    description = fields.Html(
        string='Description',
    )

    url = fields.Char(
        string='Url',
        help='More information about the OS',
    )

    # 3. Default methods

    # 4. Compute and search fields
    def _compute_display_name(self):
        for record in self:
            name = record.name

            if record.version:
                name += ' %s' % record.version

            if record.codename:
                name += ' (%s)' % record.codename

            record.display_name = name

    # 5. Constraints and onchanges
    _sql_constraints = [
        ('name_unique', 'unique(name)',
         'An operating system with this name already exists')
    ]

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
