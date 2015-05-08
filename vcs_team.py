# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.tools.translate import _

class VcsTeam(models.Model):
    
    _name = 'software_knowledge_base.vcs_team'
    _description = 'Version Control System Team'
    _order = 'name'
    
    ''' Columns '''
    name = fields.Char('Name', help='E.g. "companyname" or "teamname"')
    description = fields.Text('Description', help='Team description')