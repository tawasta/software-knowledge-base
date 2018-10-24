# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class RepositoryTag(models.Model):
    
    _name = 'software_knowledge_base.repository_tag'
    _description = 'Repository Tag'  
    _order = 'name'
    
    ''' Columns '''
    name = fields.Char('Name')
    active = fields.Boolean('Active', default=True)
    
    #parent_id = fields.Many2one('software_knowledge_base.repository_tag')
    #child_ids = fields.One2many('software_knowledge_base.repository_tag', 'id')
    
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'A tag with this name already exists')
    ]