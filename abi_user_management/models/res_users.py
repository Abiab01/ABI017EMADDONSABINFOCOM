# -*- coding: utf-8 -*-
#############################################################################
from odoo import models, fields, api
from odoo.exceptions import UserError



class ResUserInherit(models.Model):
    _inherit = 'res.users'

    visible_contact_ids = fields.Many2many(
        'res.partner',
        'partner_visible_contact_rel',
        'partner_id', 'contact_id',
        string="Visible Contact Ids",
        compute="_compute_visible_contact_ids",
        store=True,
        help="This field will give give implicit permission to other users on the basis of employee work chart.")

    def get_employee_parent_user_ids(self, employee):
        users = employee.user_id
        if employee.parent_id:
            users = users + self.get_employee_parent_user_ids(employee.parent_id)
        return users

    def get_partner_from_employee_parents(self):
        user_id = self
        employee = self.env['hr.employee'].search([('user_id', '=', user_id.id)])
        user_ids = self.get_employee_parent_user_ids(employee) - user_id
        return [user_id.partner_id.id for user_id in user_ids]

    def get_partner_from_crm_teams(self):
        user_id = self
        partners = []
        crm_teams = self.env['crm.team'].search([('type_team', '=', 'project'),('team_members_ids','in',user_id.id)])
        for crm_team in crm_teams:
            partners = partners + [member.partner_id.id for member in crm_team.team_members_ids]
            partners.append(crm_team.user_id.partner_id.id)
        return partners

    def get_partner_from_project_team_members(self):
        user_id = self
        partners = []
        crm_teams = self.env['crm.team'].search([('type_team', '=', 'project'),('team_members_ids','in',user_id.id)])
        team_projects = self.env['project.project'].search([('team_ids','in', crm_teams.ids)])
        for project in team_projects:
            partners = partners + [member.partner_id.id for member in project.members_ids] + project.message_partner_ids.ids
            partners.extend([team.user_id.partner_id.id for team in project.team_ids])

        return partners

    @api.model
    def _compute_visible_contact_ids(self):
        for user in self:
            if user.has_group('abi_user_management.group_abi_employee'):
                partner_ids = user.get_partner_from_employee_parents()
                partner_ids = partner_ids + user.get_partner_from_project_team_members()
                partner_ids = list(set(partner_ids))
                if partner_ids and user.partner_id.id in partner_ids:
                    partner_ids.remove(user.partner_id.id)
                user.visible_contact_ids = [(4, partner) for partner in partner_ids if partner]
            else:
                user.visible_contact_ids = False


    def write(self,vals):
        res = super().write(vals)
        status = any([type(key) == str and key.startswith('in_group') for key in vals.keys()])
        if status and self.has_group('abi_user_management.group_abi_employee'):
            self.search([])._compute_visible_contact_ids()
        return res


        return self.env.ref('base.view_partner_title_form').id