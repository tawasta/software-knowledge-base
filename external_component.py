# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class library(osv.Model):
    
    _name = 'software_knowledge_base.external_component'    
    _inherit = ['mail.thread']    

    _columns = {
        'name': fields.char('Name'),
        'additional_info': fields.text('Additional info'),
    }
