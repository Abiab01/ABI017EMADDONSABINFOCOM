from datetime import timedelta, datetime
import random
import logging

from odoo import models, fields, _

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    email_verified = fields.Boolean(default=False)
    otp = fields.Char()
    valid_till = fields.Datetime()

    def action_send_otp(self):
        self.ensure_one()
        otp = random.randrange(100000, 999999, 6)
        template = self.env.ref('auth_verify_email.verify_email_template', raise_if_not_found=False)
        body = f"<br/>Please find the One-Time-Password to verify your account.<br/><br/> \
            OTP - {otp} <br/><br/> \
            NOTE - Please note this OTP is valid for 10 minutes.<br/>"
        msg_id = self.env['mail.message'].sudo().create({
            'record_name': 'Verify OTP - {0}'.format(self.name),
            'body': body,
            'model': 'res.partner',
            'message_type': 'notification',
            'subject': 'Verify Email Address::OTP',
            'res_id': self.id
        })

        if template:
            ctx = {
                'message': msg_id,
                'company': self.env['res.company'].sudo().search([], limit=1)
            }
            render_template = template._render(ctx, engine='ir.qweb')
            mail_body = self.env['mail.render.mixin']._replace_local_links(render_template)
            mail_values = {
                'body_html': mail_body,
                'subject': _("Verify Email Address - OTP"),
                'email_to': self.email,
                'email_from': 'Magnetposts.com <team@magnetposts.com>',
                'author_id': self.create_uid.partner_id.id,
            }
            self.env['mail.mail'].sudo().create(mail_values).send()
            self.otp = otp
            self.valid_till = datetime.now() + timedelta(minutes=10)

    def action_verify_otp(self, otp):
        if self.otp != otp.strip():
            return {"msg": "Invalid OTP!"}
        if datetime.now() > self.valid_till:
            return {"msg": "OTP Expired!"}
        self.email_verified = True
        self.otp = False
        self.valid_till = False
        return {}
