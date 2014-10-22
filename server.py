# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class server(osv.Model):
    
    _name = 'software_knowledge_base.server'    
    _inherit = ['mail.thread']    

    _columns = {
        'name': fields.char('Name'),
        'company_id': fields.many2one('res.company', 'Company'),
        
        'ip_address': fields.char('IP Address'),
        'operating_system': fields.char('Operating system'),
        'installation_ids': fields.one2many('software_knowledge_base.installation', 'server_id', 'Installations'),
        
        'specification': fields.text('Technical specification'),
        'additional_info': fields.text('Additional info'),
    }
