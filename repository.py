# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.tools.translate import _
import urllib2

class Repository(models.Model):
    
    _name = 'software_knowledge_base.repository'
    _description = 'Repository'
    _inherit = ['mail.thread']    
    _order = 'name'
    
    ''' Columns '''
    name = fields.Char('Name', help='E.g. "odoo-customizations" or "moodle-extension"')
    description = fields.Text('Description', compute='_get_readme')
    
    url = fields.Char('URL', help='The full URL')
    url_readonly = fields.Char('URL', help='The full URL', readonly=True)
    
    vcs = fields.Many2one('software_knowledge_base.vcs', string='Type', default=lambda self: self.vcs.search([('name', '=', 'git')]) )
    vcs_host = fields.Many2one('software_knowledge_base.vcs_host', string='Host', default=lambda self: self.vcs_host.search([('name', '=', 'github')]))
    vcs_team = fields.Many2one('software_knowledge_base.vcs_team', string='Team')
    
    tag_ids = fields.Many2many('software_knowledge_base.repository_tag', 'software_knowledge_base_repository_tag_rel', 'id', 'repository_id', string='Tags')
    
    master_branch = fields.Char('Master branch', default='master')
    
    @api.one
    @api.onchange('name', 'vcs', 'vcs_team', 'vcs_host')
    def generate_url(self):
        self.url = "%s/%s/%s" % (self.vcs_host.address or '', self.vcs_team.name or '' , self.name or '')
        self.url_readonly = self.url
        
        ''' TODO: validate url structure '''
        ''' TODO: check if url exists '''
        
    @api.depends('url', 'vcs_host', 'master_branch')
    def _get_readme(self):
        target_urls = self._get_readme_urls()
        
        readme = str()
        http_response = {}

        for target_url in target_urls:
            try:
                http_response = urllib2.urlopen(target_url)
                break
            except urllib2.HTTPError:
                self.description = "README NOT FOUND"
        
        for line in http_response:
            readme += line
        
        self.description = readme

    def _get_readme_urls(self):
        vcs_type = self.vcs_host.name
        filenames = ['README.md', 'README.txt']
        
        target_urls = []
        
        for filename in filenames:
            if vcs_type == 'Gitlist':
                url_suffix = "/raw/" + self.master_branch + "/" + filename
            else:
                url_suffix = ""
    
            if self.url and url_suffix:
                target_urls.append( self.url + url_suffix )
        
        return target_urls
        
    @api.model
    def create(self, vals):
        vals['url_readonly'] = vals.get('url')
        
        return super(Repository, self).create(vals)
    
    @api.multi
    def write(self, vals):
        vals['url_readonly'] = self.url
        
        return super(Repository, self).write(vals)

    ''' TODO: This doesn't work. Add a working SQL constraint '''
    _sql_constraints = [
        ('url_unique', 'unique(url)', _('This repository already exists.'))
    ]