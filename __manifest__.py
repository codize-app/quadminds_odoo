# -*- coding: utf-8 -*-
{
    'name': "QuadMinds Odoo Connector",

    'summary': """
        Connector Odoo-QuadMinds""",

    'description': """
        Connector Odoo-QuadMinds for Pickings
    """,

    'author': "Codize",
    'website': "https://www.codize.ar",

    'category': 'Sales',
    'version': '0.1',

    'depends': ['base', 'stock'],

    'data': [
        'views/res_company.xml',
        'views/res_partner.xml',
        'views/stock_picking.xml',
    ]
}
