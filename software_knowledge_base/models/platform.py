# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class platform(models.Model):
    
    _name = 'software_knowledge_base.platform'
    _description = 'Platform'
    _inherit = ['mail.thread']    
    _order = 'name'
    
    name = fields.Char('Name', help='E.g. Odoo 8 or Drupal 7')
    description = fields.Text('Description')
    repository = fields.Many2one('software_knowledge_base.repository', string='Repository')
    active = fields.Boolean(default=True)
