##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2016 Oy Tawasta OS Technologies Ltd. (http://www.tawasta.fi)
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
    "name": "SDKB Version Control",
    "summary": "Adds version control to Software development knowledge base",
    "version": "14.0.1.0.0",
    "category": "Knowledge",
    "website": "https://gitlab.com/tawasta/odoo/software-knowledge-base",
    "author": "Tawasta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": ["software_knowledge_base"],
    "data": [
        "data/vcs_data.xml",
        "security/ir_model_access.xml",
        "views/menus.xml",
        "views/platform.xml",
        "views/repository.xml",
        "views/vcs.xml",
        "views/vcs_host.xml",
        "views/vcs_provider.xml",
        "views/vcs_team.xml",
    ],
    "demo": [],
}
