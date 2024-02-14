

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class Channel(models.Model):
    _inherit = 'discuss.channel'

    @api.model
    def create(self,vals):
        if self.env.user.has_group('abi_user_management.group_abi_employee'):
            # if channel is creating first time
            if 'channel_last_seen_partner_ids' in vals:
                if vals['channel_last_seen_partner_ids'][0][2].get('partner_id',0) in (1,2,3):
                    return super().create(vals)
            raise UserError("You Don't have permission to create a new Channel please contact your Admin")
        return super().create(vals)

    def write(self,vals):

        # user can only join and leave the channel that's why update 'channel_partner_ids'
        if any([item in vals for item in ('channel_partner_ids', 'active')]):
            return super().write(vals)
        # has_abi_employee = self.env.user.has_group('abi_user_management.group_abi_employee')
        # has_erp_manager = self.env.user.has_group('base.group_erp_manager')

        #    only admin can change the channel
        if not self.env.is_admin():
            raise UserError("You Don't have permission to Edit a Channel please contact your Admin")

        return super().write(vals)