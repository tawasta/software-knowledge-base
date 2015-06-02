# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.tools.translate import _

class VcsHost(models.Model):
    
    _name = 'software_knowledge_base.vcs_provider'
    _description = 'Version Control System Provider'
    _order = 'name'
    
    ''' Columns '''
    name = fields.Char('Name', help='E.g. github or bitbucket')
    description = fields.Text('Description', help='Longer description, if needed')
    address = fields.Char('Address', help='E.g. https://github.com or 192.168.100.100')
    
    @api.one
    def name_get(self):
        display_name = "%s (%s)" % (self.name, self.address)
        return (self.id, display_name)