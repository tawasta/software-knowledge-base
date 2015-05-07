# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.tools.translate import _

class Repository(models.Model):
    
    _name = 'software_knowledge_base.repository'
    _description = 'Repository'
    _inherit = ['mail.thread']    
    _order = 'name'
    
    ''' Columns '''
    name = fields.Char('Name', help='E.g. "Odoo customizations" or "Moodle extension"')
    description = fields.Text('Description', help='A longer description')
    type = fields.Char('Repository type', help='E.g. "git" or "svn"')
    team = fields.Char('Repository team', help='E.g. "companyname" or "teamname"')
    host = fields.Char('Repository host', help='E.g. "github" or "bitbucket"')