# -*- coding: utf-8 -*-
from odoo import models, fields, api

from odoo.exceptions import UserError

class SignTemplate(models.Model):
    _inherit = 'sign.template'

    def unlink(self):
        if not self.env.is_admin():
            raise UserError("You Don't have permission to Delete Sign Template please contact your Admin")
        return super().unlink()

    @api.model
    def create(self, vals):
        if not self.env.is_admin():
            raise UserError("You Don't have permission to create a new Sign Template please contact your Admin")
        else:
            return super().create(vals)


class SignRequest(models.Model):
    _inherit = 'sign.request'

    def unlink(self):
        if not self.env.is_admin():
            raise UserError("You Don't have permission to Delete Sign Request please contact your Admin")
        return super().unlink()

    # def create(self, vals):
    #     if not self.env.is_admin():
    #         raise UserError("You Don't have permission to create a new Sign Template please contact your Admin")
    #     else:
    #         return super().create(vals)
