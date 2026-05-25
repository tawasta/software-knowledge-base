##############################################################################
#
#    Author: Futural Oy
#    Copyright 2024 Futural Oy (https://futural.fi)
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
    "name": "Project: Require Module Info for Tasks",
    "summary": "Configure that SWKB module info has to be set before a task can "
    "moved to a certain stage",
    "version": "17.0.1.0.2",
    "category": "Project",
    "website": "https://github.com/tawasta/software-knowledge-base",
    "author": "Futural",
    "license": "AGPL-3",
    "depends": ["project_task_mattermost", "software_knowledge_base"],
    "data": ["views/project_project.xml", "views/project_task.xml"],
    "demo": [],
    "application": False,
    "installable": True,
}
