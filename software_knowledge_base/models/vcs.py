# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Vcs(models.Model):
    
    _name = 'software_knowledge_base.vcs'
    _description = 'Version Control System'
    _order = 'name'
    
    ''' Columns '''
    name = fields.Char('Name', help='E.g. git or svn')
    description = fields.Text('Description', help='The full name')
    vcs_hosts = fields.One2many('software_knowledge_base.vcs_host', 'vcs', string='VCS Hosts', readme=True)

    @api.one
    def name_get(self):
        display_name = "%s (%s)" % (self.name, self.description)
        return (self.id, display_name)