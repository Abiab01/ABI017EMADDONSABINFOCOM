

from odoo import fields, models, api, _
from odoo.exceptions import UserError



class Project(models.Model):
    _inherit = 'project.project'

    @api.model
    def unlink(self):
        if not self.env.is_admin():
            raise UserError("You Don't have permission to Delete Project please contact your Admin")
        return super().unlink()

    @api.model
    def create(self,vals):
        if "privacy_visibility" not in vals:
            vals["privacy_visibility"] = "followers"
        return super().create(vals)


    def write(self,vals):
        if "members_ids" in vals:
            old_members = self.members_ids
            res = super().write(vals)
            new_members = self.members_ids - old_members - self.env.user
            partner_ids = [member.partner_id.id for member in new_members]
            self.message_subscribe(partner_ids)
            self.members_ids._compute_visible_contact_ids()
            return res

        else:
            return  super().write(vals)

class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.model
    def unlink(self):
        if not self.env.is_admin():
            raise UserError("You Don't have permission to Delete a Task please contact your Admin")
        return super().unlink()