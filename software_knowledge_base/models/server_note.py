from odoo import fields, models


class ServerNote(models.Model):
    _name = "software_knowledge_base.server_note"
    _description = "Server notes"
    _order = "event_date DESC, create_date DESC"

    name = fields.Char(string="Short description", required=True)

    event_date = fields.Date(
        string="Event date",
        default=fields.Datetime.now(),
        help="The actual date when the operation was made",
    )

    description = fields.Text(string="Full description")

    extra = fields.Text(string="Extra info")

    server_id = fields.Many2one(
        comodel_name="software_knowledge_base.server", string="Server"
    )
