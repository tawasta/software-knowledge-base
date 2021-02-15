import base64
import logging

import gitlab

from odoo import _, api, fields, models

_logger = logging.getLogger()


class SWKBRepository(models.Model):

    _name = "software_knowledge_base.repository"
    _description = "Repository"
    _inherit = ["mail.thread"]
    _order = "name"

    name = fields.Char(
        string="Name", help='E.g. "odoo-customizations" or "moodle-extension"'
    )
    description = fields.Text(string="Description")

    readme = fields.Text(string="Readme")

    active = fields.Boolean(default=True)

    url = fields.Char(string="URL", help="The full URL")

    url_readonly = fields.Char(
        string="URL", help="The full URL", readonly=True, store=True
    )

    vcs = fields.Many2one(
        comodel_name="software_knowledge_base.vcs",
        string="Type",
        default=lambda self: self._get_default_vcs(),
    )

    vcs_host = fields.Many2one(
        comodel_name="software_knowledge_base.vcs_host",
        string="Host",
        default=lambda self: self._get_default_vcs_host(),
    )

    vcs_team = fields.Many2one(
        comodel_name="software_knowledge_base.vcs_team", string="Team"
    )

    tag_ids = fields.Many2many(
        comodel_name="software_knowledge_base.repository_tag",
        relation="software_knowledge_base_repository_tag_rel",
        column1="id",
        column2="repository_id",
        string="Tags",
    )

    master_branch = fields.Char(string="Master branch", default="master")

    def _get_default_vcs(self):
        args = [("name", "=", "git")]
        res = self.env["software_knowledge_base.vcs"].search(args)
        return res and res[0] or False

    def _get_default_vcs_host(self):
        args = [("name", "=", "Github")]
        res = self.env["software_knowledge_base.vcs_host"].search(args)
        return res and res[0] or False

    @api.onchange("name", "vcs", "vcs_team", "vcs_host")
    def onchange_repository_generate_url(self):
        self.url = "{}/{}/{}".format(
            self.vcs_host.address or "", self.vcs_team.name or "", self.name or "",
        )
        self.url_readonly = self.url

        """ TODO: validate url structure """
        """ TODO: check if url exists """

    @api.model
    def create(self, vals):
        if "url" in vals:
            vals["url_readonly"] = vals.get("url")

        return super(SWKBRepository, self).create(vals)

    @api.multi
    def write(self, vals):
        if "url" in vals:
            vals["url_readonly"] = vals["url"]

        return super(SWKBRepository, self).write(vals)

    @api.onchange("name", "vcs", "vcs_team", "vcs_host")
    def generate_url(self):
        self.url = "{}/{}/{}".format(
            self.vcs_host.address or "", self.vcs_team.name or "", self.name or "",
        )
        self.url_readonly = self.url

        """ TODO: validate url structure """
        """ TODO: check if url exists """

    @api.multi
    def action_update_readme(self):
        for record in self:
            record._get_readme()

    @api.depends("url", "vcs_host", "vcs_team", "master_branch")
    def _get_readme(self):
        for record in self:
            files = record.api_gitlab_get_files()

            record.readme = record.api_get_readme_from_repository_tree(files)

    # Gitlab
    def api_gitlab_get_session(self):
        self.ensure_one()

        host = self.vcs_host
        if not host:
            _logger.warning(_("No VCS host set: %s", self))
        session = gitlab.Gitlab(
            host.address, token=host.api_token, verify_ssl=host.api_verify_ssl
        )

        return session

    def api_gitlab_get_project(self):
        self.ensure_one()

        session = self.api_gitlab_get_session()

        project_path = "{}/{}".format(self.vcs_team.name, self.name)
        project = session.getproject(project_path)

        if not project:
            _logger.warning(_("No project found: %s" % self))
            return False

        return project

    def api_gitlab_get_files(self, *args, **kwargs):
        self.ensure_one()

        session = self.api_gitlab_get_session()
        project = self.api_gitlab_get_project()

        if not project:
            return False

        files = session.getrepositorytree(project["id"], *args, **kwargs)

        return files

    def api_gitlab_get_file(self, file_path):
        self.ensure_one()

        session = self.api_gitlab_get_session()
        project = self.api_gitlab_get_project()

        if not project:
            return False

        file = session.getfile(project["id"], file_path, project["default_branch"])

        return file

    def api_gitlab_get_readme(self):
        self.ensure_one()

        session = self.api_gitlab_get_session()
        project = self.api_gitlab_get_project()

        if not project:
            return False

        file = session.getfile(project["id"], file["path"], project["default_branch"])

        return file

    def api_get_readme_from_repository_tree(self, tree):
        if not tree:
            return False

        for file in tree:
            if file["name"][0:6].lower() == "readme":
                readme_file = self.api_gitlab_get_file(file["path"])

                readme_file_content = base64.b64decode(readme_file["content"])

                return readme_file_content

        return False
