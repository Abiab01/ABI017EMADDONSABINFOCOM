# In your_module/controllers/main.py
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

class ShopController(http.Controller):
    @http.route('/shop/address', type='json', auth='public', methods=['POST'], website=True)
    def check_email(self, **post):
        email = post.get('email')
        if request.env['res.partner'].sudo().search([('email', '=', email)], limit=1):
            return {'error': "A contact with this email already exists."}
        return {'success': True}
