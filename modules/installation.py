# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class Installation(models.Model):
    
    # 1. Private attributes
    _name = 'software_knowledge_base.installation'
    _description = 'Installation'
    _inherit = ['mail.thread']
    _order = 'name'

    _INSTALLATION_STATE_VALUES = [
        ('setup', 'In setup'),
        ('ready', 'In use'),
        ('terminated', 'Terminated')
    ]

    # 2. Fields declaration
    name = fields.Char('Name')
    company_id = fields.Many2one('res.company', 'Company')

    state = fields.Selection(
        _INSTALLATION_STATE_VALUES,
        'Status',
        help='Where the module has been developed',
        default='setup'
    )
    additional_info = fields.Text('Additional info')

    platform_id = fields.Many2one('software_knowledge_base.platform', string='Platform')
    server_id = fields.Many2one('software_knowledge_base.server', string='Server')
    port = fields.Integer('Port')
    db_server_id = fields.Many2one('software_knowledge_base.server', string='Database server')
    disk_usage = fields.Float('Disk Usage (MB)')
    url = fields.Char('URL')
    identifier = fields.Char('Identifier')

    project_ids = fields.Many2many(
        'project.project', 'installation_project_rel', 'installation_id', 'project_id',
        string='Projects', help='Projects utilizing this installation.'
    )

    # Note the misnamed table module_partner_rel!
    partner_ids = fields.Many2many(
        'res.partner', 'module_partner_rel', 'installation_id', 'partner_id',
        string='Customers', help='Customers of this installation.'
    )

    module_ids = fields.Many2many(
        'software_knowledge_base.module', 'module_installation_rel', 'installation_id', 'module_id',
        string='Modules', help='Modules used by this installation.'
    )

    external_component_ids = fields.Many2many(
        'software_knowledge_base.external_component', 'installation_ext_comp_rel', 'installation_id', 'ext_comp_id',
        string='External components', help='Libraries and other third party components used by this installation.'
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
