# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class installation(osv.Model):
    
    _name = 'software_knowledge_base.installation'    
    _inherit = ['mail.thread']    

    _columns = {
        'name':             fields.char('Name'),
        'additional_info':  fields.text('Additional info'),
        
        'platform_id':      fields.many2one('software_knowledge_base.platform', string='Platform'),
        'server_id':        fields.many2one('software_knowledge_base.server', string='Server'),
        'project_id':       fields.many2one('project.project', string='Project'),
        'partner_id':       fields.many2one('res.partner', string='Customer'),
        
        'external_component_ids': fields.many2many('software_knowledge_base.external_component', 'installation_ext_comp_rel', 'installation_id', 'ext_comp_id',
                                                 string='External components',help='Required libraries and other third party components'),        
    }
