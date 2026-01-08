# -*- coding: utf-8 -*-
{
    'name': "fp_management",

    'summary': "Gestión de estudiantes y ciclos de FP",

    'description': """
Permite la asignación de estudiantes a ciclos formativos de FP
    """,

    'author': "Daniel Castelao",
    'website': "https://www.youtube.com/watch?v=dQw4w9WgXcQ",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Education',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        "security/ir.model.access.csv",
        "views/ciclo_fp_views.xml",
        "views/estudiante_fp_views.xml",
        "views/menu.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
}

