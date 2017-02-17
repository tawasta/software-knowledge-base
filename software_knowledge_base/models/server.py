# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models


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
    name = fields.Char('Name')
    company_id = fields.Many2one('res.company', 'Company')

    ip_address = fields.Char('IP Address')
    operating_system = fields.Char('Operating system')
    installation_ids = fields.One2many('software_knowledge_base.installation', 'server_id', 'Installations')
    note_ids = fields.One2many('software_knowledge_base.server_note', 'server_id', 'Server note')

    specification = fields.Text('Technical specification')
    additional_info = fields.Text('Additional info')

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
