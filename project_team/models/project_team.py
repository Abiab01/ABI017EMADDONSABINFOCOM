# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    members_ids = fields.Many2many('res.users', 'project_team_member_rel_1', 'project_id',
                                   'user_id', 'Project Team Members', help="""Project's
                                    members are users who can have an access to
                                    the tasks related to this project.""",
                                    store=True)

    extra_member_ids = fields.Many2many('res.users', 'project_team_member_rel_2',
                                        'project_id', 'user_id',
                                        string='Additional Members', domain="[('id', 'not in', members_ids),('id', 'not in', extra_member_ids)]")

    team_ids = fields.Many2many('crm.team', string="Project Teams", domain=[('type_team', '=', 'project')])


    def _update_team_members(self):
        team_members_ids = self.team_ids.mapped("team_members_ids").ids
        team_members_ids.extend(self.extra_member_ids.ids)
        self.members_ids = [(6, False, team_members_ids)] if team_members_ids else False

    @api.onchange('team_ids', 'extra_member_ids')
    def _onchange_project_team_ids(self):
        self._update_team_members()

    def write(self,vals):
        res = super().write(vals)
        if ("team_ids" in vals) or ('extra_member_ids' in vals):
            self._update_team_members()
        return res