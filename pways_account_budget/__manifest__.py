# -*- coding: utf-8 -*-

{
    'name': 'Budgets Management',
    'category': 'Accounting',
    'version':'18.0.0.0',
    'summary': 'Budgets Management with Analytic Accounts',
    'description': """ Analytic Accounts Budgets Management""",
    'author': 'Preciseways',
    'website': 'http://www.preciseways.com',
    'depends': ['account', 'base'],
    "price": 0.0,
    "currency": 'EUR',
    'data': [
        'security/ir.model.access.csv',
        'security/account_budget_security.xml',
        'views/account_analytic_account_views.xml',
        'views/account_budget_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'demo': ['data/account_budget_demo.xml'],
    'license': 'OPL-1',

}
