# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class module(osv.Model):
    
    _name       = 'software_knowledge_base.module'
    _description = 'Module' 
    _inherit    = ['mail.thread']    

    _MODULE_TYPE_VALUES = [('core','Core'),
                    ('community','Community'),
                    ('inhouse','In-house')]

    _columns = {
        'name':                 fields.char('Name'),
        'module_type':          fields.selection(_MODULE_TYPE_VALUES, 'Module type', help='Where the module has been developed'),
        'repository':           fields.char('Repository URL', help='Version control location'),
        
        'features':             fields.text('Features'),
        'installation_notes':   fields.text('Installation notes'),
        'issues':               fields.text('Issues', help='Known bugs, limitations, incompatibilities with other modules etc.'),
        'additional_info':      fields.text('Additional info', help='Additional information'),
        
        'installation_ids':     fields.many2many('software_knowledge_base.installation', 'module_installation_rel', 'module_id', 'installation_id',
                                                 string='Installations', help='Where this module has been deployed.'), 
                
        #'parent_ids':           fields.many2many(
        #                            'software_knowledge_base.module',
        #                            'module_dependency_rel',
        #                            'child_id',
        #                            'parent_id',
        #                            'Dependencies', help='Other modules that are required for this module to work.'),       
                
        'task_ids':             fields.many2many('project.task', 'module_task_rel', 'module_id', 'task_id',
                                                 string='Tasks', help='Related project management tasks'),
        'platform_ids':         fields.many2many('software_knowledge_base.platform', 'module_platform_rel', 'module_id', 'platform_id',
                                                 string='Platforms',help='Supported platforms'),
    }
