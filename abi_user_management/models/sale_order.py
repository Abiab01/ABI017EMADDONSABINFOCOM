# -*- coding: utf-8 -*-
#############################################################################
from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    other_user_ids = fields.Many2many(
        'res.users',
        'sale_order_other_users_rel',
        'sale_order_id', 'user_id',
        string='Other Salespersons',
        domain="['&', ('share', '=', False), ('company_ids', 'in', user_company_ids)]",
        check_company=True, index=True, tracking=True)
