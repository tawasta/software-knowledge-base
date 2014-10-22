# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class platform(osv.Model):
    
    _name = 'software_knowledge_base.platform'
    _description = 'Platform'
    _inherit = ['mail.thread']    

    _columns = {
        'name': fields.char('Name', help='E.g. Odoo 8 or Drupal 7'),
    }
