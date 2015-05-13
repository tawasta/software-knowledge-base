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
    description = fields.Text('Description', help='Longer description')
    url = fields.Char('URL', help='The full URL')
    url_readonly = fields.Char('URL', help='The full URL', readonly=True)
    vcs = fields.Many2one('software_knowledge_base.vcs', string='Type', default=lambda self: self.vcs.search([('name', '=', 'git')]) )
    vcs_host = fields.Many2one('software_knowledge_base.vcs_host', string='Host', default=lambda self: self.vcs_host.search([('name', '=', 'github')]))
    vcs_team = fields.Many2one('software_knowledge_base.vcs_team', string='Team')
    
    ''' TODO: add repository tags? '''
    
    @api.one
    @api.onchange('name', 'vcs', 'vcs_team', 'vcs_host')
    def generate_url(self):
        self.url = "%s/%s/%s" % (self.vcs_host.address or '', self.vcs_team.name or '' , self.name or '')
        self.url_readonly = self.url
        
        ''' TODO: validate url structure '''
        ''' TODO: check if url exists '''
        
    @api.multi
    def write(self, vals):
        vals['url_readonly'] = self.url
        
        return super(Repository, self).write(vals)
    
    ''' TODO: This doesn't work. Add a working SQL constraint '''
    _sql_constraints = [
        ('url_unique', 'unique(url)', _('This repository already exists.'))
    ]