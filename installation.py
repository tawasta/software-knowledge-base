# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class installation(osv.Model):
    
    _name = 'software_knowledge_base.installation'
    _description = 'Installation'  
    _inherit = ['mail.thread']    
    _order = 'name'
    
    _INSTALLATION_STATE_VALUES = [('setup','In setup'),
                                  ('ready','In use'),
                                  ('terminated','Terminated')]
    
    _columns = {
        'name':             fields.char('Name'),
        'company_id': fields.many2one('res.company', 'Company'),
        
        'state':            fields.selection(_INSTALLATION_STATE_VALUES, 'Status', help='Where the module has been developed'),
        'additional_info':  fields.text('Additional info'),
        
        'platform_id':      fields.many2one('software_knowledge_base.platform', string='Platform'),
        'server_id':        fields.many2one('software_knowledge_base.server', string='Server'),
        'port':             fields.integer('Port'),
        'db_server_id':     fields.many2one('software_knowledge_base.server', string='Database server'),
        
        #'project_id':       fields.many2one('project.project', string='Project'),
        'project_ids':     fields.many2many('project.project', 'installation_project_rel', 'installation_id', 'project_id',
                                                 string='Projects', help='Projects utilizing this installation.'),
                        

        'partner_id':       fields.many2one('res.partner', string='Customer'),
        
        'module_ids':     fields.many2many('software_knowledge_base.module', 'module_installation_rel', 'installation_id', 'module_id',
                                                 string='Modules', help='Modules used by this installation.'),
                        
        'external_component_ids': fields.many2many('software_knowledge_base.external_component', 'installation_ext_comp_rel', 'installation_id', 'ext_comp_id',
                                                 string='External components',help='Libraries and other third party components used by this installation.'),        
    }
    
    _defaults = {
        'state': 'setup',
    }
