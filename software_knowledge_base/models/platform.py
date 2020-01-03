# -*- coding: utf-8 -*-
from odoo import models, fields


class Platform(models.Model):

    _name = 'software_knowledge_base.platform'
    _description = 'Platform'
    _inherit = ['mail.thread']    
    _order = 'name'

    active = fields.Boolean(
        default=True,
    )

    name = fields.Char(
        string='Name',
        help='E.g. Odoo 10 or Drupal 8'
    )

    description = fields.Text(
        string='Description'
    )

    repository = fields.Many2one(
        comodel_name='software_knowledge_base.repository',
        string='Repository'
    )

    active = fields.Boolean(
        default=True
    )
