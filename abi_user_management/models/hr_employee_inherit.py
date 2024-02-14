from odoo import fields, models, api, _
from odoo.exceptions import UserError
import logging


_logger = logging.getLogger(__name__)


class EmployeeInherit(models.Model):
    _inherit = 'hr.department'

    # def user_group_domain(self):
    #     internal_group = self.env.ref('base.group_user')
    #     portal_group = self.env.ref('base.group_portal')
    #     internal_user_groups = [group.id for group in internal_group.implied_ids]
    #     portal_user_groups = [group.id for group in portal_group.implied_ids]
    #     internal_user_groups.append(internal_group.id)
    #     portal_user_groups.append(portal_group.id)
    #     renu_group_list = [self.env.ref(group_name).id for group_name in groups_name_list]
    #     return [('id', 'not in',internal_user_groups + portal_user_groups + renu_group_list)]

    # user_groups_id = fields.Many2many('res.groups', string="User Groups", domain=user_group_domain)
    user_groups_id = fields.Many2many('res.groups', string="User Groups",)


