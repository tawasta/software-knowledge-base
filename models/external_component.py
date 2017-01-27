# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class external_component(osv.Model):
    
    _name = 'software_knowledge_base.external_component'
    _description = 'External component'
    _inherit = ['mail.thread']    
    _order = 'name'
    
    _columns = {
        'name': fields.char('Name'),
        'url': fields.char('Homepage'),
        'features': fields.text('Features'),

        'installation_ids': fields.many2many('software_knowledge_base.installation', 'installation_ext_comp_rel', 'ext_comp_id', 'installation_id',
                                                 string='Installations',help='Installations using this component.'),

        'installation_notes':   fields.text('Installation notes'),
        'additional_info':      fields.text('Additional info', help='Additional information'),               
    }
