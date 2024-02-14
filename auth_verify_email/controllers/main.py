import logging
import json

from odoo import http, _
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.http import request

_logger = logging.getLogger(__name__)


class AuthSignupExtended(AuthSignupHome):

    @http.route([
        '/verify/email'
    ], type='http', auth="user", website=True, sitemap=True, csrf=True)
    def verify_user_creds(self, **kw):
        resp = {"status": True}
        partner_id = request.env.user.partner_id
        if kw.get('otp'):
            _r = partner_id.action_verify_otp(kw.get('otp'))
            if _r.get('msg'):
                resp['error'] = _r.get('msg')
            else:
                resp['reload'] = True
        else:
            partner_id.action_send_otp()
        return json.dumps(resp)