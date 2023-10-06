from odoo import fields, models


class Installation(models.Model):

    _inherit = "software_knowledge_base.installation"


    technical_responsible_person_id = fields.Many2one(string="Technical responsible person", comodel_name="res.users")
