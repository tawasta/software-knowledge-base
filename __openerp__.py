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
    'version': '0.1',
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
 * Work in progress ...


""",
    'data': [
        'view/installation.xml',
        'view/module.xml',
        'view/server.xml',
        'view/external_component.xml',
        'view/project_project.xml',
        'view/menus.xml',
    ],
}
