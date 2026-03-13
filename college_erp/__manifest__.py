{
    'name': 'College ERP',
    'version': '18.0.1.1',
    'license': 'LGPL-3',
    'author': 'Neema Mwende',
    'category': 'Education',
    'summary': 'An erp for college education',
    'description': """From students administration to exam, this covers all aspects of college administratioon""",
    'website': 'https://github.com/NeemaMwende',
    'maintainer': 'Mi casa su casa <neemamwende009@gmail.com>',
    'sequence': 1,
    'data': [
        'security/ir.model.access.csv',
        'views/college_student_view.xml',
        'views/college_erp_menus.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': True
}
