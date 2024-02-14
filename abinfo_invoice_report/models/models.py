# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveInherited(models.Model):
    _inherit = 'account.move'

    invoice_type = fields.Selection([
        ('b2b', 'B2B'),
        ('b2c', 'B2C')
    ], compute='compute_invoice_type', store=True)
    invoice_area_type = fields.Selection([
        ('intra_state', 'Intra State'),
        ('inter_state', 'Inter State'),
        ('international', 'International')
    ], compute='compute_invoice_area_type', store=True)
    partner_state_id = fields.Many2one('res.country.state', related='partner_id.state_id')

    @api.depends('partner_id', 'partner_state_id')
    def compute_invoice_area_type(self):
        for rec in self:
            if rec.partner_state_id.country_id.id != rec.company_id.country_id.id:
                rec.invoice_area_type = 'international'
            elif rec.partner_state_id.id != rec.company_id.state_id.id:
                rec.invoice_area_type = 'inter_state'
            else:
                rec.invoice_area_type = 'intra_state'

    @api.depends('partner_id')
    def compute_invoice_type(self):
        for rec in self:
            rec.invoice_type = 'b2b' if rec.partner_id.company_type == 'company' else 'b2c'
