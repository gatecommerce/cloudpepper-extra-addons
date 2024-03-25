# -*- coding: utf-8 -*-
{
    'name': "Relationships & Data Model",

    'summary': """
        odoo database architecture, odoo er diagram, Odoo Data Model: Models Relationships and Diagram - a game-changing Odoo addon that revolutionizes how you visualize Odoo models as elegant ER diagrams, er diagram, entity relation, relationship, data mode, data models, modelling, modeling, related columns, foreign key, primary key, one to one, one to many, many to one, many to many, one2one, one2many, many2many, schema powerbi, power bi, tableau, looker, bigquery, big query, dashboard, dashboard ninja, connector, connecter, relationship viewer, analyzer, dataset, database, model relationship, models.
""",

    'description': """
        Odoo Data Model: Models Relationships and Diagram - a game-changing Odoo addon that revolutionizes how you visualize Odoo models as elegant ER diagrams

    """,

    'author': "TechFinna",
    'website': "https://techfinna.com/",
    'category': 'Productivity',
    'price': 129,
    'currency': 'USD',
    'version': '2.0',
    'installable': True,
    'live_test_url': 'https://demo.techfinna.com',
    'support': "info@techfinna.com",
    'application': True,
    'auto_install': False,
    'license': 'OPL-1',
    'depends': ['base','web'],
    'images': ['static/description/banner.gif'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/menu.xml',
        'security/ir.model.access.csv',
        'views/query_dashboard.xml'
    ],
    'assets': {
        'odoodatamodel.erassets': [
            'odoodatamodel/static/backend/css/*',
            'odoodatamodel/static/backend/js/*',
        ],
        'odoodatamodel.mtass': [
            'odoodatamodel/static/minitab/js/c3.min.js',
            'odoodatamodel/static/minitab/js/chart.js',
            'odoodatamodel/static/minitab/js/main.js',
            'odoodatamodel/static/minitab/js/other.js',
            'odoodatamodel/static/minitab/scss/*',

        ]

    },
    # only loaded in demonstration mode
    "application": True,
    "installable": True,
}
