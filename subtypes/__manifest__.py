# -*- coding: utf-8 -*-
{
    'name': "Custom helpdesk for OpenBlue",
    'summary': """Ticket query subtypes""",
    'description': """
        Ticket query subtypes
    """,
    'author': "PSDC Inc. & Eric Dominguez",
    'website': "https://www.psdc.com.pa",
    'category': 'Other',
    'version': '1.0.0',
    'depends': ['helpdesk'],
    'data': [
        'views/ticket_subtypes.xml',
        'views/team_subtypes.xml',
        # 'views/ticket_products.xml'
    ]
}
