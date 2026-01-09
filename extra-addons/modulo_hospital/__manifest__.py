# -*- coding: utf-8 -*-
{
    'name': "modulo_hospital",

    'summary': "Gestión de médicos y pacientes de un hospital",

    'description': """
Modulo que gestiona la interacción entre pacientes y médicos y el diagnóstico que este les da.
    """,

    'author': "CabbaGG Corp.",
    'website': "https://www.rickroll.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Healthcare',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/paciente_hospital_views.xml',
        'views/medico_hospital_views.xml',
        'views/diagnostico_hospital_views.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

