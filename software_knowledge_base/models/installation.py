# -*- coding: utf-8 -*-
from openerp import api, fields, models


class Installation(models.Model):
    _name = 'software_knowledge_base.installation'
    _description = 'Installation'
    _inherit = ['mail.thread']
    _order = 'name'

    _INSTALLATION_STATE_VALUES = [
        ('setup', 'In setup'),
        ('ready', 'In use'),
        ('terminated', 'Terminated')
    ]

    _INSTALLATION_TYPE_VALUES = [
        ('dev', 'Dev'),
        ('test', 'Test'),
        ('staging', 'Staging'),
        ('production', 'Production'),
    ]

    name = fields.Char('Name')
    company_id = fields.Many2one('res.company', 'Company')

    state = fields.Selection(
        _INSTALLATION_STATE_VALUES,
        'Status',
        help='What is the deployments status of the installation',
        default='setup'
    )
    type = fields.Selection(
        selection=_INSTALLATION_TYPE_VALUES,
        string='Type',
    )

    additional_info = fields.Text('Additional info')

    platform_id = fields.Many2one('software_knowledge_base.platform', string='Platform')

    server_id = fields.Many2one('software_knowledge_base.server', string='Server')
    server_ip_address = fields.Char('Server IP-address', related='server_id.ip_address')

    port = fields.Integer('Port')

    db_server_id = fields.Many2one('software_knowledge_base.server', string='Database server')
    db_server_ip_address = fields.Char('DB server IP-address', related='db_server_id.ip_address')

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