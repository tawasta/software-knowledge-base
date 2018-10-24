# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class VcsHost(models.Model):
    
    _name = 'software_knowledge_base.vcs_host'
    _description = 'Version Control System Host'
    _order = 'name'
    
    ''' Columns '''
    name = fields.Char('Name', help='E.g. github or bitbucket')
    vcs = fields.Many2one('software_knowledge_base.vcs', string='VCS', required=True)
    repositories = fields.One2many('software_knowledge_base.repository', 'vcs_host', string='Repositories', readonly=True)
    description = fields.Text('Description', help='Longer description, if needed')
    address = fields.Char('Address', help='E.g. https://github.com or 192.168.100.100')
    address_readme = fields.Char('Readme Address', help='E.g. https://raw.githubusercontent.com')
    #provider = fields.Many2one('software_knowledge_base.vcs_provider', string='Provider')

    @api.one
    def name_get(self):
        display_name = "%s (%s)" % (self.name, self.address)
        return (self.id, display_name)