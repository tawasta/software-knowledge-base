# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Vizucom Oy
#    Copyright 2016 Vizucom Oy (http://www.vizucom.com)
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
    'name': 'Software development knowledge base',
    'summary': 'A module for maintaining data regarding software installations and modules',
    'version': '8.0.1.1.3',
    'category': 'Knowledge',
    'website': 'http://www.vizucom.com',
    'author': 'Vizucom Oy',
    'license': 'AGPL-3',
    'application': True,
    'installable': True,
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    'depends': [
        'project',
    ],
    'data': [
        'data/ir_module_category.xml',
        'data/res_groups.xml',
        'data/vcs_data.xml',
        'data/vcs_host_data.xml',

        'security/ir.model.access.csv',

        'views/menus.xml',
        'views/external_component.xml',
        'views/installation.xml',
        'views/menus.xml',
        'views/module.xml',
        'views/operating_system.xml',
        'views/platform.xml',
        'views/project_project.xml',
        'views/project_task.xml',
        'views/repository.xml',
        'views/res_partner.xml',
        'views/server_note.xml',
        'views/server.xml',
        'views/vcs_host.xml',
        'views/vcs_team.xml',
        'views/vcs.xml',
        # 'views/vcs_provider.xml',
    ],
    'demo': [
    ],
}