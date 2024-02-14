# -*- coding: utf-8 -*-
#############################################################################
from odoo import models, fields, api


class CRM(models.Model):
    _inherit = "crm.lead"

    other_user_ids = fields.Many2many(
        'res.users', string='Other Salespersons',domain="['&', ('share', '=', False), ('company_ids', 'in', user_company_ids)]",
        check_company=True, index=True, tracking=True)

    is_sales_person_not_in_customer = fields.Boolean(compute="_check_missing_sale_persons", store=True)

    @api.depends("partner_id", 'user_id','other_user_ids', "partner_id.other_user_ids")
    def _check_missing_sale_persons(self):
        for lead in self:
            if lead.partner_id:
                c_sp_ids = lead.partner_id.other_user_ids + lead.partner_id.user_id
                lead_cp_ids = lead.other_user_ids + lead.user_id
                if any([lead_sp not in c_sp_ids for lead_sp in lead_cp_ids]):
                    lead.is_sales_person_not_in_customer = True
                else:
                    lead.is_sales_person_not_in_customer = False

            else:
                lead.is_sales_person_not_in_customer = False