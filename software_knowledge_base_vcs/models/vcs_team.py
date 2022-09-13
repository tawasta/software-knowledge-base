from odoo import fields, models


class VcsTeam(models.Model):
    _name = "software_knowledge_base.vcs_team"
    _description = "Version Control System Team"
    _order = "name"

    name = fields.Char(string="Name", help='E.g. "companyname" or "teamname"')
    description = fields.Text(string="Description", help="Team description")
