.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================================
Software development knowledge base
===================================

A module for maintaining data regarding software installations and modules. Built mainly around the needs
of a Odoo development company, but if you do module-based software development and offer cloud services,
you may find this it useful for other platforms as well.

Features
--------

Adds the following models for storing and organizing development-related data:

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

Links installations to projects and partners

Access rights
-------------
* By default, all Odoo users have read access to knowledge base items.
* Creates two new groups: Developer and Administrator
* Administrators have full create/write/unlink access to all knowledge base items
* Developers have otherwise full access but they cannot create or unlink installations, servers or platforms.

Installation
============

Install the module form Settings->Local Modules

Configuration
=============
\-

Usage
=====
\-

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Jarmo Kortetjärvi <jarmo.kortetjarvi@tawasta.fi>
* Timo Talvitie <timo.talvitie@vizucom.com>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
