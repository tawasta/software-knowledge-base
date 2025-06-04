.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================================
Project: Require Module Info for Tasks
======================================

* Enables configuring task stages that require Software Knowledge Base modules to be set

Configuration
=============

* Go to a project's settings and select the stages in Task Stages Requiring Module Info field.
* The project's tasks cannot be moved to these stages unless either

  * Module info has been set for the task
  * The task's "This Task did not Involve Modules" field has been checked.

Usage
=====

* Apply the above configuration to a project, and try to move a task to a stage
  without the appropriate module info. An error is shown and stage change is prevented.
* If you created a new module, you can manually run the "Software knowledge base:
  export information" cron in the customer installation to get the module to immediately
  show up in Software Knowledge Base's list of modules.

Known issues / Roadmap
======================
* None

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
