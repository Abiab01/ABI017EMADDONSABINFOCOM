# -*- coding: utf-8 -*-
{
    'name': "Verify Email Address",
    'description': """
        This app send the email verification link to the newly registered user to verify the email.    
    """,
    'version': '17.0.0.2',
    'summary': '',
    "author": "Abinfocom",
    "website": "www.abinfocom.com",
    'category': 'Website',
    'depends': ['auth_signup', 'website', 'mail', 'base', 'base_vat'],
    'data': [
        # 'security/ir.model.access.csv',
        'data/mail_template.xml',
        # 'views/res_partner_view.xml',
        'views/email_template.xml',
        # 'views/template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/auth_verify_email/static/src/scss/verify_mail.scss',
            '/auth_verify_email/static/src/js/verify_mail.js',
            '/auth_verify_email/static/src/js/email_verify_otp.js',
            '/auth_verify_email/static/src/js/zip_length.js',
        ],
    },
    'demo': [
        # 'demo/demo.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True
}
