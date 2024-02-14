# import json
# from werkzeug.utils import redirect
#
# from odoo import http, registry
# from odoo.http import request
# from odoo.addons.appointments.controllers.google_oauth_inherit import GoogleAuthInherit
#
#
# class GoogleAuthInherit(GoogleAuthInherit):
#     @http.route('/google_account/authentication', type='http', auth="public")
#     def oauth2callback(self, **kw):
#         """ This route/function is called by Google when user Accept/Refuse the consent of Google """
#         state = json.loads(kw['state'])
#         if not state.get('user_id'):
#             return super(GoogleAuthInherit, self).oauth2callback(**kw)
#         dbname = state.get('d')
#         service = state.get('s')
#         url_return = state.get('f')
#
#         with registry(dbname).cursor() as cr:
#             if kw.get('code'):
#                 access_token, refresh_token, ttl = request.env['google.service']._get_google_tokens(kw['code'], service)
#                 if state.get('s') == 'workspace':
#                     request.env.user.sudo().browse(state.get('user_id'))._set_workspace_auth_tokens(access_token, refresh_token, ttl)
#                 else:
#                     request.env.user.sudo().browse(state.get('user_id'))._set_auth_tokens(access_token, refresh_token, ttl)
#                 return redirect(url_return)
#             elif kw.get('error'):
#                 return redirect("%s%s%s" % (url_return, "?error=", kw['error']))
#             else:
#                 return redirect("%s%s" % (url_return, "?error=Unknown_error"))
