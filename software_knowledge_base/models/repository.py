# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, fields, models


# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SWKBRepository(models.Model):

    # 1. Private attributes
    _name = 'software_knowledge_base.repository'
    _description = 'Repository'
    _inherit = ['mail.thread']
    _order = 'name'

    # 2. Fields declaration
    name = fields.Char(
        string='Name',
        help='E.g. "odoo-customizations" or "moodle-extension"'
    )
    description = fields.Text(
        string='Description'
    )

    readme = fields.Text(
        string='Readme'
    )

    active = fields.Boolean(
        default=True
    )

    url = fields.Char(
        string='URL',
        help='The full URL'
    )

    url_readonly = fields.Char(
        string='URL',
        help='The full URL',
        readonly=True,
        store=True
    )

    vcs = fields.Many2one(
        comodel_name='software_knowledge_base.vcs',
        string='Type',
        default=lambda self: self.vcs.search([('name', '=', 'git')])
    )

    vcs_host = fields.Many2one(
        comodel_name='software_knowledge_base.vcs_host',
        string='Host',
        default=lambda self: self.vcs_host.search([('name', '=', 'github')])
    )

    vcs_team = fields.Many2one(
        comodel_name='software_knowledge_base.vcs_team',
        string='Team'
    )

    tag_ids = fields.Many2many(
        comodel_name='software_knowledge_base.repository_tag',
        relation='software_knowledge_base_repository_tag_rel',
        column1='id',
        column2='repository_id',
        string='Tags'
    )

    master_branch = fields.Char(
        string='Master branch',
        default='master'
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges
    @api.one
    @api.onchange('name', 'vcs', 'vcs_team', 'vcs_host')
    def onchange_repository_generate_url(self):
        self.url = "%s/%s/%s" % (self.vcs_host.address or '',
                                 self.vcs_team.name or '', self.name or '')
        self.url_readonly = self.url

        ''' TODO: validate url structure '''
        ''' TODO: check if url exists '''

    # 6. CRUD methods
    @api.model
    def create(self, vals):
        if 'url' in vals:
            vals['url_readonly'] = vals.get('url')

        return super(SWKBRepository, self).create(vals)

    @api.multi
    def write(self, vals):
        if 'url' in vals:
            vals['url_readonly'] = vals['url']

        return super(SWKBRepository, self).write(vals)

    # 7. Action methods

    # 8. Business methods
    @api.one
    @api.onchange('name', 'vcs', 'vcs_team', 'vcs_host')
    def generate_url(self):
        self.url = "%s/%s/%s" % (self.vcs_host.address or '',
                                 self.vcs_team.name or '', self.name or '')
        self.url_readonly = self.url

        ''' TODO: validate url structure '''
        ''' TODO: check if url exists '''
