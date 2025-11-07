.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================
SWKB Capabilities
=================

This module extends the **Software Knowledge Base** by introducing the concept of
**Capabilities** – logical business or functional areas that describe what an
installation or customer setup is capable of.

A capability groups together the Odoo modules required to provide a certain
functionality (for example, Sales, CRM, or Project Management).  
Capabilities can also include other capabilities, forming a hierarchy of related
features.  

By linking capabilities to an installation, both technical and non-technical users
can clearly understand **what kind of system configuration** a customer has,
and which modules are needed to support those capabilities.

Installation
============

1. Ensure the base module ``software_knowledge_base`` is installed.
2. Install this module from the Apps menu or by updating your custom add-ons.

Configuration
=============

No special configuration is required.

You can immediately start defining capabilities under:
**Knowledge Base → Capabilities → Manage**.

Each capability record allows you to:
- Name and describe the capability
- Define required modules
- Optionally include other capabilities
- View all resolved modules (direct + included)

Usage
=====

1. Create one or more **Capabilities**, e.g. “Sales Operations” or “Customer Portal”.
2. For each capability, add its required modules in the *Modules* tab.
3. Link capabilities to **Installations** to describe what that installation includes.
4. Open an installation form and use the **Capabilities** stat button to review
   or apply capability sets through the *Apply Capabilities* wizard.

This makes it easier to:
- Communicate to non-technical users what the installation provides.
- Automatically determine which modules should be installed.
- Standardize and speed up new system setups.

Example
-------

**Capability:** *Sales Operations*  
Includes:
- CRM  
- Sales  
- Contact Management  

→ The resolved module list automatically combines all related modules
from this and any included capabilities.

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
