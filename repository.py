# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.tools.translate import _

class Repository(models.Model):
    
    _name = 'software_knowledge_base.repository'
    _description = 'Repository'
    _inherit = ['mail.thread']    
    _order = 'name'
    
    ''' Columns '''
    name = fields.Char('Name', help='E.g. "odoo-customizations" or "moodle-extension"')
    description = fields.Char('Description', help='Full name or description')
    url = fields.Char('URL', help='The full URL')
    vcs = fields.Many2one('software_knowledge_base.vcs', string='Type', default='git')
    vcs_host = fields.Many2one('software_knowledge_base.vcs_host', string='Host', default='Github')
    vcs_team = fields.Many2one('software_knowledge_base.vcs_team', string='Team')
        
    @api.one
    @api.onchange('name', 'team', 'vcs', 'vcs_host')
    def generate_url(self):
        self.url = "%s/%s/%s" % (self.vcs_host.address or '', self.vcs_team.name or '' , self.name or '')
        
        ''' TODO: validate url structure '''
        ''' TODO: check if url exists '''