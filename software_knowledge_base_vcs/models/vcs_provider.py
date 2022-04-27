from odoo import api, fields, models


class VcsProvider(models.Model):
    _name = "software_knowledge_base.vcs_provider"
    _description = "Version Control System Provider"
    _order = "name"

    name = fields.Char(string="Name", help="E.g. github or bitbucket")
    description = fields.Text(
        string="Description", help="Longer description, if needed"
    )

    address = fields.Char(
        string="Address", help="E.g. https://github.com or 192.168.100.100"
    )

    def name_get(self):
        res = []
        for record in self:
            display_name = "{} ({})".format(record.name, record.address)
            res.append((record.id, display_name))

        return res
