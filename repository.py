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
    name = fields.Char('Name',
                       help='E.g. "odoo-customizations" or "moodle-extension"')
    description = fields.Text('Description')
    readme = fields.Text('Readme', compute='_get_readme', store=True)

    url = fields.Char('URL', help='The full URL')
    url_readonly = fields.Char('URL', help='The full URL',
                               readonly=True, store=True)

    vcs = fields.Many2one('software_knowledge_base.vcs', string='Type',
                          default=lambda self:
                          self.vcs.search([('name', '=', 'git')]))
    vcs_host = fields.Many2one('software_knowledge_base.vcs_host',
                               string='Host',
                               default=lambda self:
                               self.vcs_host.search([('name', '=', 'github')]))
    vcs_team = fields.Many2one('software_knowledge_base.vcs_team',
                               string='Team')

    tag_ids = fields.Many2many('software_knowledge_base.repository_tag',
                               'software_knowledge_base_repository_tag_rel',
                               'id', 'repository_id', string='Tags')

    master_branch = fields.Char('Master branch', default='master')

    @api.one
    @api.onchange('name', 'vcs', 'vcs_team', 'vcs_host')
    def generate_url(self):
        self.url = "%s/%s/%s" % (self.vcs_host.address or '',
                                 self.vcs_team.name or '', self.name or '')
        self.url_readonly = self.url

        ''' TODO: validate url structure '''
        ''' TODO: check if url exists '''

    @api.depends('url', 'vcs_host', 'vcs_team', 'master_branch')
    def _get_readme(self):
        if not self.vcs_host.readme_autofetch:
            return False

        target_urls = self._get_readme_urls()

        readme = str()
        http_response = {}

        for target_url in target_urls:
            try:
                http_response = urllib2.urlopen(target_url)
            except urllib2.HTTPError:
                self.readme = "README NOT FOUND"

        for line in http_response:
            readme += line

        self.readme = readme

    def _get_readme_urls(self):
        vcs_host = self.vcs_host.name

        filenames = ['README.md', 'README.rst', 'README.txt']
        url_prefix = self.url

        target_urls = []

        for filename in filenames:
            if vcs_host == 'Github':
                url_prefix = "%s/%s/%s" % ("https://raw.githubusercontent.com",
                                           self.vcs_team.name, self.name)
                url_suffix = "/%s/%s" % (self.master_branch, filename)

            elif vcs_host == 'Gitlist':
                url_suffix = "/raw/" + self.master_branch + "/" + filename

            else:
                url_suffix = ""

            if url_prefix and url_suffix:
                target_urls.append(url_prefix + url_suffix)

        return target_urls

    @api.model
    def create(self, vals):
        if 'url' in vals:
            vals['url_readonly'] = vals.get('url')

        return super(Repository, self).create(vals)

    @api.multi
    def write(self, vals):
        if 'url' in vals:
            vals['url_readonly'] = vals['url']

        return super(Repository, self).write(vals)

    ''' TODO: This doesn't work. Add a working SQL constraint '''
    _sql_constraints = [
        ('url_unique', 'unique(url)', _('This repository already exists.'))
    ]
