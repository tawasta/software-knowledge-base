# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.tools.translate import _

class Vcs(models.Model):
    
    _name = 'software_knowledge_base.vcs'
    _description = 'Version Control System'
    _order = 'name'
    
    ''' Columns '''
    name = fields.Char('Name', help='E.g. git or svn')
    description = fields.Text('Description', help='The full name')
    display_name = fields.Char(string='Name', compute='_compute_display_name')

    @api.one
    @api.depends('name', 'description')
    def _compute_display_name(self):
        self.display_name = "%s (%s)" % (self.name, self.description)