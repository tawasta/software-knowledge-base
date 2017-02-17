# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class server_note(osv.Model):
    
    _name = 'software_knowledge_base.server_note'       
    _order = 'event_date DESC, create_date DESC'

    _columns = {
        'name': fields.char('Short description', required=True),
        'event_date': fields.date('Event date', help='The actual date when the operation was made'),
        'description': fields.text('Full description'),
        'extra': fields.text('Extra info'),
        
        'server_id': fields.many2one('software_knowledge_base.server', string='Server'),
    }
    
    _defaults = {
        'event_date': fields.datetime.now,
    }
