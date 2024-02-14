from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CustomContact(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals):
        # Checking for duplicate email
        if 'email' in vals and vals['email']:
            existing_email = self.search([('email', '=', vals['email'])])
            if existing_email:
                raise ValidationError("A contact with this email already exists. Please enter a different email.")

        # Checking for duplicate mobile number
        if 'phone' in vals and vals['phone']:
            existing_mobile = self.search([('phone', '=', vals['phone'])])
            if existing_mobile:
                raise ValidationError("A contact with this mobile number already exists. Please enter a different mobile number.")

        # Checking for duplicate name
        if 'name' in vals and vals['name']:
            existing_name = self.search([('name', '=', vals['name'])])
            if existing_name:
                raise ValidationError("A contact with this name already exists. Please enter a different name.")

        return super(CustomContact, self).create(vals)
