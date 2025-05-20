from odoo import api, fields, models


class SoftwareKnowledgeBaseServer(models.Model):
    _name = "software_knowledge_base.server"
    _description = "Server"
    _inherit = ["mail.thread"]
    _order = "name"

    name = fields.Char(string="Name")

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.user.company_id.id,
    )

    active = fields.Boolean(string="Active", default=True)

    ip_address = fields.Char(string="IP Address")

    operating_system = fields.Char(
        string="Operating system (DEPRECATED)", readonly=True
    )

    # Please maintain an alphabetical order here
    server_type = fields.Selection(
        [
            ("application", "Application server"),
            ("database", "Database server"),
            ("dhcp", "DHCP server"),
            ("dns", "DNS server"),
            ("file", "File server"),
            ("mail", "Mail server"),
            ("other", "Other server"),
            ("print", "Print server"),
            ("proxy", "Proxy server"),
            ("web", "Web server"),
        ],
        string="Server type",
    )

    operating_system_id = fields.Many2one(
        comodel_name="software_knowledge_base.operating_system",
        string="Operating system",
        tracking=True,
    )

    installation_ids = fields.One2many(
        comodel_name="software_knowledge_base.installation",
        inverse_name="server_id",
        string="Installations",
        domain=[("state", "!=", "terminated")],
    )

    db_connections_available = fields.Integer(
        "DB Connections",
        help="Available DB connections",
    )
    db_connections_used = fields.Integer(
        "DB Connections",
        help="Available DB connections",
    )
    db_installation_ids = fields.One2many(
        comodel_name="software_knowledge_base.installation",
        inverse_name="db_server_id",
        string="DB Installations",
        domain=[("state", "!=", "terminated")],
    )

    note_ids = fields.One2many(
        comodel_name="software_knowledge_base.server_note",
        inverse_name="server_id",
        string="Server note",
    )

    cpu_cores = fields.Integer("CPU Cores")
    ram = fields.Integer("RAM (Gb)")

    disk_size = fields.Float("Disk size (Gb)")
    disk_used = fields.Float(
        "Used disk (Gb)",
        compute="_compute_disk_usage",
    )
    disk_available = fields.Float(
        "Available disk (Gb)",
        compute="_compute_disk_usage",
    )
    disk_usage_percent = fields.Float(
        string="Disk usage %", compute="_compute_disk_usage"
    )

    specification = fields.Text(string="Technical specification")

    additional_info = fields.Text(string="Additional info")

    supplier_id = fields.Many2one(
        string="Supplier",
        comodel_name="res.partner",
        help="The supplier of this server",
        domain=[("is_company", "=", True), ("supplier_rank", ">", 0)],
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsible",
        help="Appointed responsible person for this server",
        default=lambda self: self.env.user,
        tracking=True,
    )

    @api.depends("disk_size", "disk_used")
    def _compute_disk_usage(self):
        for record in self:
            record.disk_used = sum(record.installation_ids.mapped("disk_usage"))
            record.disk_available = record.disk_size - record.disk_used

            disk_usage_percent = 0
            if record.disk_size and record.disk_used > 0:
                disk_usage_percent = record.disk_used / record.disk_size * 100

            record.disk_usage_percent = disk_usage_percent
