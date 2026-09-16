.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================================
Software Knowledge Base Critical Notes
======================================

This module adds notes to Software Knowledge Base installations, and
shows the critical ones as a warning on every task or ticket linked to
that installation - since a "ticket" in this system is just a
``project.task`` on a helpdesk-flagged project, this covers both.

An installation can have any number of notes. Only notes marked
**Critical** are surfaced to tasks; other notes are reference
information visible only on the installation record itself.

Installation
============
\-

Configuration
=============
* Open an installation and use its **Notes** tab to add notes. Check
  **Critical** on the ones that must always be noticed by whoever picks
  up related work.
* Use the installation's **Show critical note alerts on tasks** checkbox
  to silence the alert for that installation without deleting its notes.

Usage
=====
* Any task or ticket whose installation has an enabled critical note
  shows a red warning banner when opened, a warning marker on its kanban
  card, and a "Critical Notes" count badge in the task list view.
* Non-critical notes are not shown on tasks - only on the installation's
  own **Notes** tab.
* Marking a note critical, unmarking it, or editing a critical note's
  title or description posts a message on the installation's own
  chatter, so there is a visible audit trail of who changed what and
  when.

Known issues / Roadmap
======================
* There is no acknowledgement/read-tracking for critical notes - the
  banner is always shown, on every open, to everyone. This is
  intentional: the alert must not be dismissible and then forgotten.

Credits
=======

Contributors
------------
* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
