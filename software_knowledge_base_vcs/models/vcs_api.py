from odoo import fields, models


class SWKBVcsApi(models.Model):
    _name = "software_knowledge_base.vcs_api"

    name = fields.Char("VCS API name", readonly=True)
    code = fields.Char("VCS API code", readonly=True)
