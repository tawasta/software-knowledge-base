# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.tools.translate import _

class Vcs(models.Model):
    
    _name = 'software_knowledge_base.vcs'
    _description = 'Version Control System'
    
    ''' Columns '''
    name = fields.Char('Name', help='E.g. git or svn')
    description = fields.Text('Description', help='The full name')