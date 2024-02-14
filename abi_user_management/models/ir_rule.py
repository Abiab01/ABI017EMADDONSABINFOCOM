# coding: utf-8
from odoo import api, models


class IrRuleInherit(models.Model):
    _inherit = 'ir.rule'

    @api.model
    def _remove_default_odoo_record_rules(self):
        project_task_rule = self.env.ref("project.task_visibility_rule",False)
        if project_task_rule:
            project_task_rule.sudo().active = False



    @api.model
    def _remove_group_from_menu(self):
        contact_menu = self.env.ref("contacts.menu_contacts", False)
        if contact_menu:
            contact_menu.groups_id = [(3,self.env.ref('base.group_user').id)]


