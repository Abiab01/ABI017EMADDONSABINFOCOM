from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    code = fields.Char("Customer Unique Id")
    code_for_vendor = fields.Char("Vendor Unique Id")
    is_seq_auto_create = fields.Boolean(compute="_compute_sequence_creation")

    def _compute_sequence_creation(self):
        for partner in self:
            partner.is_seq_auto_create = (
                self.env["ir.config_parameter"].sudo().get_param("abi_customer_sequence.is_seq_auto_create")
            )

    @api.model
    def create(self, vals):
        partner = super().create(vals)
        if partner.is_seq_auto_create:
            if partner.customer_rank > 0:
                partner.code = self.env["ir.sequence"].next_by_code("code.res.partner")
            if partner.supplier_rank > 0:
                partner.code_for_vendor = self.env["ir.sequence"].next_by_code("code.res.vendor")
        return partner

    def create_code(self):
        if self.customer_rank > 0:
            self.code = self.env["ir.sequence"].next_by_code("code.res.partner")
        if self.supplier_rank > 0:
            self.code_for_vendor = self.env["ir.sequence"].next_by_code("code.res.vendor")
