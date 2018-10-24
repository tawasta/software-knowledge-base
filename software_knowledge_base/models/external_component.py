# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SWKBExternalComponent(models.Model):

    # 1. Private attributes
    _name = 'software_knowledge_base.external_component'
    _description = 'External component'
    _inherit = ['mail.thread']
    _order = 'name'

    # 2. Fields declaration
    name = fields.Char(
        string='Name'
    )

    url = fields.Char(
        string='Homepage'
    )
    features = fields.Text(
        string='Features'
    )

    installation_ids = fields.Many2many(
        comodel_name='software_knowledge_base.installation',
        relation='installation_ext_comp_rel',
        column1='ext_comp_id',
        column2='installation_id',
        string='Installations',
        help='Installations using this component.'
    )

    installation_notes = fields.Text(
        string='Installation notes'
    )

    additional_info = fields.Text(
        string='Additional info',
        help='Additional information'
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
