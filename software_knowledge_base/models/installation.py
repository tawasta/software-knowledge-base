# -*- coding: utf-8 -*-
from odoo import fields, models


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

    active = fields.Boolean(
        default=True,
    )

    name = fields.Char(
        string='Name'
    )

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company'
    )

    state = fields.Selection(
        selection=_INSTALLATION_STATE_VALUES,
        string='Status',
        help='What is the deployments status of the installation',
        default='setup'
    )

    type = fields.Selection(
        selection=_INSTALLATION_TYPE_VALUES,
        string='Type'
    )

    additional_info = fields.Text(
        string='Additional info'
    )

    platform_id = fields.Many2one(
        comodel_name='software_knowledge_base.platform',
        string='Platform'
    )

    server_id = fields.Many2one(
        comodel_name='software_knowledge_base.server',
        string='Server'
    )

    server_ip_address = fields.Char(
        string='Server IP-address',
        related='server_id.ip_address',
        store=True,
    )

    port = fields.Integer(
        string='Port'
    )

    db_server_id = fields.Many2one(
        comodel_name='software_knowledge_base.server',
        string='Database server'
    )

    db_server_ip_address = fields.Char(
        string='DB server IP-address',
        related='db_server_id.ip_address',
        store = True,
    )

    disk_usage = fields.Float(
        string='Disk Usage (MB)'
    )

    url = fields.Char(
        string='URL'
    )

    identifier = fields.Char(
        string='Identifier'
    )
    user_accounts_total = fields.Integer(
        string='Total User Accounts'
    )
    user_accounts_active = fields.Integer(
        string='Active User Accounts',
    )
    user_accounts_active_interval = fields.Integer(
        string='Active Interval',
        default='6',
    )
    user_accounts_active_type = fields.Selection(
        selection=[
            ('days', 'Days'),
            ('weeks', 'Weeks'),
            ('months', 'Months')
        ],
        string='Interval Unit',
        default='months',
    )

    project_ids = fields.Many2many(
        comodel_name='project.project',
        relation='installation_project_rel',
        column1='installation_id',
        column2='project_id',
        string='Projects',
        help='Projects utilizing this installation.'
    )

    # Note the misnamed table module_partner_rel!
    partner_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='module_partner_rel',
        column1='installation_id',
        column2='partner_id',
        string='Customers',
        help='Customers of this installation.'
    )

    module_ids = fields.Many2many(
        comodel_name='software_knowledge_base.module',
        relation='module_installation_rel',
        column1='installation_id',
        column2='module_id',
        string='Modules',
        help='Modules used by this installation.'
    )

    external_component_ids = fields.Many2many(
        comodel_name='software_knowledge_base.external_component',
        relation='installation_ext_comp_rel',
        column1='installation_id',
        column2='ext_comp_id',
        string='External components',
        help=('Libraries and other third party components used by this '
              'installation.')
    )
