# -*- coding: utf-8 -*-
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
    'name': 'Software development knowledge base',
    'summary': 'Maintain software installation and module data',
    'version': '10.0.1.2.0',
    'category': 'Specific Industry Applications',
    'website': 'http://www.tawasta.fi',
    'author': 'Oy Tawasta Technologies Ltd.',
    'license': 'AGPL-3',
    'application': False,
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