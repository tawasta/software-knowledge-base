# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class server_log(osv.Model):
    
    _name = 'software_knowledge_base.server_log'       

    _columns = {
        'name': fields.char('Name'),
        'log_date': fields.date('Log date'),
        'description': fields.text('Longer description'),
        'extra': fields.text('Extra info (ex. commands used)'),
        
        'server_id': fields.many2one('software_knowledge_base.server', string='Server'),
    }
