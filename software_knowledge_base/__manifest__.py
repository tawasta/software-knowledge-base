##############################################################################
#
#    Author: Futural Oy
#    Copyright 2021- Futural Oy (https://futural.fi)
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

{
    "name": "Software Development Knowledge Base",
    "summary": "Maintain software installation and module data",
    "version": "17.0.1.0.7",
    "category": "Knowledge",
    "website": "https://github.com/tawasta/software-knowledge-base",
    "author": "Futural",
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "depends": ["contacts", "project"],
    "data": [
        "data/ir_cron.xml",
        "data/ir_module_category.xml",
        "data/res_groups.xml",
        "security/ir_model_access.xml",
        "views/menus.xml",
        "views/external_component.xml",
        "views/installation_form.xml",
        "views/installation_kanban.xml",
        "views/installation_search.xml",
        "views/installation_tree.xml",
        "views/module.xml",
        "views/operating_system.xml",
        "views/platform.xml",
        "views/project_project.xml",
        "views/project_task.xml",
        "views/res_partner.xml",
        "views/server_form.xml",
        "views/server_note.xml",
        "views/server_search.xml",
        "views/server_tree.xml",
        "wizards/module_merge_wizard.xml",
    ],
}
