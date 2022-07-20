import logging

import gitlab

from odoo import models

_logger = logging.getLogger()


class VcsHost(models.Model):
    _inherit = "software_knowledge_base.vcs_host"

    def gitlab_update_repositories(self):
        self.ensure_one()
        gl = self.gitlab_auth()

        _logger.info(gl.groups.list())

        projects = gl.projects.list()
        for project in projects:
            _logger.info(project)

    def gitlab_auth(self):
        self.ensure_one()
        if self.api_token:
            gl = gitlab.Gitlab(self.address, private_token=self.api_token)
        else:
            gl = gitlab.Gitlab(self.address)

        return gl
