# -*- coding: utf-8 -*-
from odoo import models, fields, _


class ServerNote(models.Model):

    _name = 'software_knowledge_base.server_note'
    _order = 'event_date DESC, create_date DESC'

    name = fields.Char('Short description', required=True)
    event_date = fields.Date('Event date', help='The actual date when the operation was made')
    description = fields.Text('Full description')
    extra = fields.Text('Extra info')
    server_id = fields.Many2one('software_knowledge_base.server', string='Server')

    # TODO port to new api syntax
    # _defaults = {
    #    'event_date': fields.datetime.now,
    # }
