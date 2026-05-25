.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================================
Software Knowledge Base: Capabilities
=====================================

This module extends **software_knowledge_base** by introducing **Capabilities**:
business/functional profiles that describe what an installation is meant to do,
and which Odoo modules it requires. Capabilities can include other capabilities,
and their required modules are automatically **resolved** (direct + included).

Key Features
============

- **Capability model (`swkb.capability`)**
  - Name, description, active
  - One2many **Module Requirements** (`swkb.capability.requirement`)
  - Many2many **Included Capabilities** (composition)
  - Computed **Resolved Modules** (union of direct + included requirements)

- **Installation integration**
  - **One2many Capability lines** (`swkb.capability.installation.line`) on
    `software_knowledge_base.installation`, each linking a capability and a
    **status** field with values:
    - ``not installed`` / ``installed``
  - **Stat button** “Capabilities” on the Installation form
    (opens capability-related information for that installation)

- **TODO: Capability Application Automation**
  - Future development will include the ability to automatically apply
    and synchronize capabilities across installations.
  - This will include secure, token-based communication and controlled
    automation for module installation and verification.

Installation
============

1. Make sure **software_knowledge_base** is installed.
2. Place this add-on in your add-ons path and update the Apps list.
3. Install **Software Knowledge Base: Capabilities**.

Configuration
=============

No special configuration is required for the base functionality.

Usage
=====

Define Capabilities
-------------------

1. Go to **Software KB → Capabilities → Manage** and create a capability.
2. Add **Module Requirements** by selecting modules (technical names, e.g. ``crm``, ``sale_management``).
3. Optionally add **Included Capabilities** to build a composition.
4. The **Resolved Modules** tab shows the combined result.

Link to Installation
--------------------

1. Open an **Installation** and add **capability lines** on the **Capabilities** tab
   (each line links one capability).
2. The line’s **Status** shows ``not installed`` or ``installed``.

Future Development
==================

In upcoming versions, the module will include:
- Automated capability synchronization between installations
- Secure, token-authenticated communication for controlled remote actions
- Enhanced visibility and reporting for applied capabilities


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

This module is maintained by **Futural Oy**.
