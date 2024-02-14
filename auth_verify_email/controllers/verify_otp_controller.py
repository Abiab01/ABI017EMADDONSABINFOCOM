from odoo import http
from odoo.http import request
import random
import logging
from datetime import datetime, timedelta
from odoo.tools.translate import _
from odoo.addons.auth_signup.controllers.main import AuthSignupHome as Home
import json

_logger = logging.getLogger(__name__)


class UserOTPController(http.Controller):
    @http.route('/user/send_otp', type='json', auth="public", website=True)
    def send_otp(self, email, **kwargs):
        otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
        valid_until = datetime.now() + timedelta(minutes=1)
        request.session[f'otp_{email}'] = {'otp': otp, 'valid_until': valid_until.isoformat()}

        _logger.info("Generated OTP: %s for email: %s", otp, email)

        mail_message_model = request.env['mail.message'].sudo()
        mail_mail_model = request.env['mail.mail'].sudo()
        current_user = request.env.user

        try:
            # Fetch the email template
            template = request.env.ref('auth_verify_email.otp_email_template', raise_if_not_found=False)
            if not template:
                _logger.error("Email template not found.")
                return {'status': 'error', 'message': 'Email template not found.'}

            # Create a message for the history (optional)
            body = f"<br/>Please find the One-Time-Password to verify your account.<br/><br/>OTP - {otp}<br/><br/>NOTE - Please note this OTP is valid for 10 minutes.<br/>"
            msg_id = mail_message_model.create({
                'record_name': f'Login OTP',
                'body': body,
                'model': 'res.users',
                'message_type': 'comment',
                'subject': 'Verify Email Address::OTP',
            })

            # Prepare mail values
            ctx = {
                'message': msg_id,
                'company': request.env['res.company'].sudo().search([], limit=1),
                'otp': otp,  # Adding OTP to the context
            }
            render_template = template._render(ctx, engine='ir.qweb')
            mail_body = request.env['mail.render.mixin']._replace_local_links(render_template)
            mail_values = {
                'subject': _("Your Login - OTP"),
                'body_html': mail_body,
                'email_to': email,
                'email_from': current_user.email_formatted or 'noreply@example.com',
                'author_id': current_user.partner_id.id,
            }

            # Create and send email
            mail = mail_mail_model.create(mail_values)
            mail.send()

            _logger.info("OTP email sent successfully to: %s", email)
            return {'status': 'success', 'message': 'OTP Sent Successfully To Your Email Address.'}
        except Exception as e:
            _logger.exception("Error when trying to send OTP email: %s", e)
            return {'status': 'error', 'message': 'Failed to send OTP. Please check logs for details.'}

    @http.route('/user/validate_otp', type='json', auth="public", website=True)
    def validate_otp(self, email, otp_provided, **kwargs):
        session_key = f'otp_{email}'
        otp_info = request.session.get(session_key)

        if not otp_info:
            return {'status': 'error', 'message': 'No OTP found for this email.'}

        stored_otp, valid_until, failed_attempts = otp_info['otp'], datetime.fromisoformat(
            otp_info['valid_until']), otp_info.get('failed_attempts', 0)

        if datetime.now() > valid_until:
            return {'status': 'error', 'message': 'OTP expired.'}

        if int(otp_provided) == stored_otp:
            # Reset failed_attempts on successful validation
            otp_info['failed_attempts'] = 0
            request.session[session_key] = otp_info
            return {'status': 'success', 'message': 'OTP is valid.'}
        else:
            # Increment failed_attempts on failed validation
            otp_info['failed_attempts'] = failed_attempts + 1
            request.session[session_key] = otp_info
            return {'status': 'error', 'message': 'Invalid OTP.', 'failed_attempts': failed_attempts + 1}


    @http.route('/user/resend_otp', type='json', auth="public", website=True)
    def resend_otp(self, email, **kwargs):
        session_key = f'otp_{email}'
        if session_key not in request.session:
            return {'status': 'error', 'message': 'No OTP request found.'}

        # Retrieve the OTP information from the session
        last_otp_info = request.session[session_key]
        # Convert the valid_until string back to a datetime object
        valid_until = datetime.fromisoformat(last_otp_info['valid_until'])
        if datetime.now() <= valid_until:
            # If the current time is before the valid_until time, don't allow resend yet
            return {'status': 'error', 'message': 'Please wait before requesting a new OTP.'}

        # Send a new OTP
        return self.send_otp(email)


