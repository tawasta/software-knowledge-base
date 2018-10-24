# -*- coding: utf-8 -*-
from odoo import models, fields, api, _



class module(models.Model):
    
    _name           = 'software_knowledge_base.module'
    _description    = 'Module' 
    _inherit        = ['mail.thread']
    _order          = 'name'

    _MODULE_TYPE_VALUES = [('core','Core'),
                    ('community','Community'),
                    ('community_commercial','Community (commercial)'),                    
                    ('inhouse','In-house')]

    name = fields.Char('Name')
    summary = fields.Char(size=128, string='Summary')
    module_type = fields.Selection(_MODULE_TYPE_VALUES, 'Module type', help='Where the module has been developed')
    repository = fields.Many2one('software_knowledge_base.repository', string='Repository')
    user_id = fields.Many2one('res.users', 'Responsible')
    features = fields.Text('Features')
    readme = fields.Text('Readme')
    installation_notes = fields.Text('Installation notes')
    issues = fields.Text('Issues', help='Known bugs, limitations, incompatibilities with other modules etc.')
    additional_info = fields.Text('Additional info', help='Additional information')
    active = fields.Boolean(default=True)
    
    installation_ids = fields.Many2many('software_knowledge_base.installation', 'module_installation_rel', 'module_id', 'installation_id',
                                             string='Installations', help='Where this module has been deployed.')
            
    #'parent_ids'=           fields.many2many(
    #                            'software_knowledge_base.module',
    #                            'module_dependency_rel',
    #                            'child_id',
    #                            'parent_id',
    #                            'Dependencies', help='Other modules that are required for this module to work.'),       
            
    task_ids =             fields.Many2many('project.task', 'module_task_rel', 'module_id', 'task_id',
                                             string='Tasks', help='Related project management tasks')
    platform_ids =         fields.Many2many('software_knowledge_base.platform', 'module_platform_rel', 'module_id', 'platform_id',
                                                 string='Platforms',help='Supported platforms')
