##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2021- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class Module(models.Model):
    # 1. Private attributes
    _name = "software_knowledge_base.module"
    _description = "Module"
    _inherit = ["mail.thread"]
    _order = "name"

    _MODULE_TYPE_VALUES = [
        ("core", "Core"),
        ("community", "Community"),
        ("community_commercial", "Community (commercial)"),
        ("inhouse", "In-house"),
        ("inhouse_commercial", "In-house (commercial)"),
    ]

    # 2. Fields declaration
    name = fields.Char(string="Name")
    description = fields.Char(string="Description")
    author = fields.Char(string="Author")
    website = fields.Char(string="Website")
    summary = fields.Char(size=128, string="Summary")

    module_type = fields.Selection(
        selection=_MODULE_TYPE_VALUES,
        string="Module type",
        help="Where the module has been developed",
    )

    user_id = fields.Many2one(comodel_name="res.users", string="Responsible")

    features = fields.Text(string="Features")

    readme = fields.Text(string="Readme")

    installation_notes = fields.Text(string="Installation notes")

    issues = fields.Text(
        string="Issues",
        help=("Known bugs, limitations, incompatibilities with other " "modules etc."),
    )

    additional_info = fields.Text(
        string="Additional info", help="Additional information"
    )

    active = fields.Boolean(default=True)

    installation_ids = fields.Many2many(
        comodel_name="software_knowledge_base.installation",
        relation="module_installation_rel",
        column1="module_id",
        column2="installation_id",
        string="Installations",
        help="Where this module has been deployed.",
    )

    installation_count = fields.Integer(
        "Installation count", compute="_compute_installation_count"
    )

    task_ids = fields.Many2many(
        comodel_name="project.task",
        relation="module_task_rel",
        column1="module_id",
        column2="task_id",
        string="Tasks",
        help="Related project management tasks",
    )

    platform_ids = fields.Many2many(
        comodel_name="software_knowledge_base.platform",
        relation="module_platform_rel",
        column1="module_id",
        column2="platform_id",
        string="Platforms",
        help="Supported platforms",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    def _compute_installation_count(self):
        for record in self:
            record.installation_count = len(record.installation_ids)

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
