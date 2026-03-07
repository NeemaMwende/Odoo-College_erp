{
    'name': 'Metabase Connector (JWT Embed)',
    'version': '18.0.1.0.0',
    'summary': 'Embed interactive Metabase dashboards in Odoo using JWT signed embedding',
    'description': """
        Metabase JWT Embed Connector for Odoo 18
        =========================================
        - Configure Metabase connection (URL + Secret Key)
        - Register dashboards by Metabase ID
        - Generate JWT tokens for secure, interactive embedding
        - Full drill-down and filter support in embedded dashboards
        - Dynamically create Odoo menu items for dashboards
    """,
    'author': 'Sortprime',
    'category': 'Reporting',
    'depends': ['base', 'web'],
    'external_dependencies': {
        'python': ['PyJWT'],
    },
    'data': [
        'security/ir.model.access.csv',
        'views/metabase_config_views.xml',
        'views/metabase_dashboard_views.xml',
        'views/metabase_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'metabase_connector2/static/src/css/metabase.css',
            'metabase_connector2/static/src/js/metabase_dashboard.xml',
            'metabase_connector2/static/src/js/metabase_dashboard.js',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
