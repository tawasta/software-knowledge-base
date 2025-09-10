from odoo import fields, models


class SWKBOperatingSystem(models.Model):
    _name = "software_knowledge_base.operating_system"
    _description = "Operating system"
    _order = "name"

    display_name = fields.Char(compute="_compute_display_name")

    server_ids = fields.One2many(
        comodel_name="software_knowledge_base.server",
        inverse_name="operating_system_id",
        string="Servers",
    )

    name = fields.Char(help='E.g. "Debian" or "CentOS"')

    active = fields.Boolean(default=True)

    version = fields.Char()

    codename = fields.Char(help='E.g. "Buster" or "Zapus"')

    description = fields.Html()

    url = fields.Char(string="URL", help="More information about the OS")

    def _compute_display_name(self):
        for record in self:
            name = record.name

            if record.version:
                name += " %s" % record.version

            if record.codename:
                name += " (%s)" % record.codename

            record.display_name = name

    _sql_constraints = [
        (
            "name_unique",
            "unique(name)",
            "An operating system with this name already exists",
        )
    ]
