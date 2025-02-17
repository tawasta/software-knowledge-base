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

# 6. Unknown third party imports:
import logging

# 3. Odoo imports (openerp):
from odoo import fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:


_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    # 1. Private attributes
    _inherit = "project.task"

    # 2. Fields declaration
    module_ids = fields.Many2many(
        comodel_name="software_knowledge_base.module",
        relation="module_task_rel",
        column1="task_id",
        column2="module_id",
        string="Modules",
        help="List here the modules that were affected by the work done in this task. "
        "If you created a new module, you can manually run the 'Software knowledge "
        "'base: export information' cron in the customer installation to get the "
        "module to immediately show up in Software Knowledge Base's list of modules.",
    )

    module_count = fields.Integer(
        string="Module count", compute="_compute_module_count"
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    def _compute_module_count(self):
        for record in self:
            record.module_count = len(record.module_ids)

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def action_view_modules(self):
        _logger.info("action reached")
        _logger.info(self.module_ids.ids)
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "software_knowledge_base.modules_action"
        )
        action["domain"] = [("id", "in", self.module_ids.ids)]
        return action

    # 8. Business methods
