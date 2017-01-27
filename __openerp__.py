# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2014- Vizucom Oy (http://www.vizucom.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Software development knowledge base',
    'category': 'Knowledge',
    'version': '8.0.1.0.2',
    'author': 'Vizucom Oy',
    'website': 'http://www.vizucom.com',    
    'depends': ['project'],
    'description': """
SW Development knowledge base
=============================
A module for maintaining data regarding software installations and modules. Built mainly around the needs
of a Odoo development company, but if you do module-based software development and offer cloud services,
you may find this it useful for other platforms as well.

Features
--------
 * Adds the following models for storing and organizing development-related data:
  * server
  * server note
  * installation
  * platform
  * module
  * external component
  * repository
  * repository tags
  * vcs
  * vcs host
 * Links installations to projects and partners 

Access rights
-------------
 * By default, all Odoo users have read access to knowledge base items.
 * Creates two new groups: Developer and Administrator
 * Administrators have full create/write/unlink access to all knowledge base items
 * Developers have otherwise full access but they cannot create or unlink installations, servers or platforms.

""",
    'data': [
        'views/installation.xml',
        'views/module.xml',
        'views/server.xml',
        'views/server_note.xml',
        'views/external_component.xml',
        'views/platform.xml',
        'views/repository.xml',
        'views/vcs.xml',
        #'views/vcs_provider.xml',
        'views/vcs_host.xml',
        'views/vcs_team.xml',
        'views/project_project.xml',
        'views/project_task.xml',
        'views/res_partner.xml',
        'data/ir_module_category.xml',
        'data/res_groups.xml',
        'security/ir.model.access.csv',
        'views/menus.xml',
        'data/installation_data_copy.xml',
        'data/vcs_data.xml',
        'data/vcs_host_data.xml',
    ],
}
