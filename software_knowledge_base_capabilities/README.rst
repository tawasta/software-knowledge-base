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

An **Apply Capabilities** wizard is added to the Installation form. It can
authenticate to a **remote client database** (via XML-RPC) and install the
modules required by the selected capabilities. The wizard shows step-by-step
notifications (auth OK → wait → start → results) and reports *missing*,
*already installed*, and *installed* modules. After a successful run, the
linked capability line on the installation is marked **asennettu** (installed).

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
    - ``ei asennettu`` / ``asennettu`` (not_installed / installed)
  - **Stat button** “Capabilities” to open the **Apply Capabilities** wizard

- **Apply Capabilities wizard**
  - Lists capabilities from the installation’s **capability lines**
    (O2M; shows resolved modules per capability)
  - Authenticates to a **remote Odoo** via XML-RPC
  - Sends webclient toasts (auth OK, starting, already installed, missing, success)
  - Installs only modules not yet installed (Odoo handles dependencies)
  - After success, sets the selected capability lines’ **status = asennettu**

Installation
============

1. Make sure **software_knowledge_base** is installed.
2. Place this add-on in your add-ons path and update the Apps list.
3. Install **Software Knowledge Base: Capabilities**.

Configuration
=============

**System Parameters (set in the SWKB instance):**

- ``skb_capabilities.client_user`` → remote client username (e.g. ``admin``)
- ``skb_capabilities.client_key`` → remote client password or API key

**Installation record (in the SWKB instance):**

- ``admin_url`` (or ``url``): remote base URL (e.g. ``http://localhost:8069``)
- ``identifier``: remote database name (e.g. ``client``)

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
2. The line’s **Status** shows ``ei asennettu`` or ``asennettu``.

Apply Capabilities (Remote Install)
-----------------------------------

1. Click the **Capabilities** stat button to open the wizard.
2. In the wizard, tick the capabilities you want to apply (**Apply** = True).
3. Click **Apply**. You will see toasts for:
   - **Connection OK** (authentication succeeded)
   - (about 4 seconds later) **Starting installation…**
   - **Already installed** / **Missing modules in client**
   - **Success** (install completed)
4. After a successful run, the selected capability lines on the installation are
   marked **asennettu**.

Security
========

- RPC credentials are read from **ir.config_parameter** on the SWKB instance.
- Protect ``skb_capabilities.client_key``; installing modules requires admin privileges.
- Ensure the installation’s ``admin_url``/``identifier`` match the client.

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
