{
    'name': 'Abi User Management',
    'version': '17.0.1.0.0',
    'summary': 'This module will manage the user permission on the basis of custom fields and record rules',
    'description': """This module will manage the user permission on the basis of custom fields and record rules""",
    'live_test_url': '',
    'category': 'ABI Extra Tools',
    'author': 'Abinfocom',
    'maintainer': 'Team Abinfocom',
    'company': 'Abinfocom',
    'website': 'https://www.abinfocom.com/apps',
    'license': 'LGPL-3',
    'depends': ['hr', 'hr_timesheet', 'sale', 'crm', 'documents_sign', 'helpdesk', "auth_oauth"],

    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'data/data.xml',
        'views/hr_employee_inherit.xml',
        'views/partner_views.xml',
        'views/sale_order_views.xml',
        'views/crm_lead_views.xml',

    ],
    'qweb': [],
    'installable': True,
    'application': False,
}
