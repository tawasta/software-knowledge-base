# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, fields, models


# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SoftwareKnowledgeBaseServer(models.Model):
    # 1. Private attributes
    _name = 'software_knowledge_base.server'
    _description = 'Server'
    _inherit = ['mail.thread']
    _order = 'name'

    # 2. Fields declaration
    name = fields.Char(
        string='Name'
    )

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env['res.users'].browse(
            [self._uid]).company_id,
    )

    active = fields.Boolean(
        string='Active',
        default=True,
    )

    ip_address = fields.Char(
        string='IP Address',
    )

    operating_system = fields.Char(
        string='Operating system (DEPRECATED)',
        readonly=True,
    )

    operating_system_id = fields.Many2one(
        comodel_name='software_knowledge_base.operating_system',
        string='Operating system',
    )

    installation_ids = fields.One2many(
        comodel_name='software_knowledge_base.installation',
        inverse_name='server_id',
        string='Installations',
        domain=[('state', '!=', 'terminated')],
    )

    note_ids = fields.One2many(
        comodel_name='software_knowledge_base.server_note',
        inverse_name='server_id',
        string='Server note',
    )

    specification = fields.Text(
        string='Technical specification',
    )

    additional_info = fields.Text(
        string='Additional info'
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
