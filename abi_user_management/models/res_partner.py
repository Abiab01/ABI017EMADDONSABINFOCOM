# -*- coding: utf-8 -*-
#############################################################################
from odoo import models, fields, api
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    other_user_ids = fields.Many2many(
        'res.users',
        'partner_other_users_rel',
        'partner_id', 'user_id',
        string='Other Salespersons',
        domain="['&', ('share', '=', False), ('company_ids', 'in', user_company_ids)]",
        check_company=True, index=True, tracking=True)

    visible_to_users = fields.Many2many(
        'res.users',
        'partner_visible_users_rel',
        'partner_id', 'user_id',
        string="Visible To Users",
        compute="_compute_visible_to_user_ids",
        store=True,
        help="This field will give implicit permission to other users on the basis of employee work chart.")


    def get_employee_parent_user_ids(self, employee):
        users = employee.user_id
        if employee.parent_id:
            users = users + self.get_employee_parent_user_ids(employee.parent_id)
        return users

    def assign_visible_to_users_records(self):
        if self.user_id:
            self.visible_to_users = False
            employee = self.env['hr.employee'].search([('user_id', '=', self.user_id.id)])
            user_ids = self.get_employee_parent_user_ids(employee) - self.user_id
            # contact.visible_to_users = False
            self.visible_to_users = [(4, user_id) for user_id in user_ids.ids]
        else:
            self.visible_to_users = False
        # self.env.cr.commit()

    @api.depends('user_id')
    def _compute_visible_to_user_ids(self):
        for contact in self:
            contact.assign_visible_to_users_records()

    @api.onchange('parent_id', 'company_id')
    def _onchange_company_id(self):
        if self.parent_id:
            if any([self.parent_id.id == comp.partner_id.id for comp in self.env.user.company_ids]):
                raise UserError("You are not allowed to set root company as a company in any contact, "
                                "please contact your admin")

    def write(self, vals):
        rec = super().write(vals)
        if vals.get('user_id'):
            self.assign_visible_to_users_records()

        return rec

    @api.model
    def create(self,vals):
        if type(vals) == list:
            for val in vals:
                if 'user_id' not in val:
                    val['user_id'] = self.env.user.id
        elif 'user_id' not in vals:
            vals['user_id'] = self.env.user.id

        return super().create(vals)



    def get_formview_id(self, access_uid=None):
        """ Override this method in order to redirect many2one towards the right model depending on access_uid """
        if access_uid:
            self_sudo = self.with_user(access_uid)
        else:
            self_sudo = self

        if self_sudo.check_access_rights('read', raise_exception=False):
            return super(ResPartner, self).get_formview_id(access_uid=access_uid)
        # Hardcode the form view for public employee
        return self.env.ref('base.view_partner_title_form').id
