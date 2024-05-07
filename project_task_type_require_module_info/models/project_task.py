from odoo import _, fields, models
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):

    _inherit = "project.task"

    task_did_not_involve_modules = fields.Boolean(
        string="This Task did not Involve Modules",
        help="No module-related work was required to complete this task.",
    )

    def write(self, vals):
        """
        Check if task stage can be changed, or if module info is missing. Only
        enforce the limitation to internal users.
        """
        res = super(ProjectTask, self).write(vals)
        if vals.get("stage_id") and self.env.user.has_group("base.group_user"):
            for task in self:
                stage_ids_requiring_modules = [
                    s.id for s in task.project_id.module_info_required_stage_ids
                ]
                if (
                    task.stage_id.id in stage_ids_requiring_modules
                    and not task.task_did_not_involve_modules
                ):
                    raise ValidationError(
                        _(
                            "Please fill in the Module information before moving the "
                            "task to this stage. Or if no modules were involved, check "
                            "the 'This Task did not Involve Modules' box."
                        )
                    )

        return res
