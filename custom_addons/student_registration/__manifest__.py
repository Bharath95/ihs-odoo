# -*- coding: utf-8 -*-
{
    'name': 'Student Registration',
    'version': '1.0',
    'summary': 'Student Registration and Admission Form',
    'description': """
        This module provides functionality for student registration and admission process.
        Features include:
        - Student registration form
        - Personal information management
        - Academic history tracking
        - Health records
        - Parent/Guardian details
        - Payment and billing information
    """,
    'category': 'Education',
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': [
        'base',
        'web',
        'mail',
        'portal',
    ],
    'data': [
        # 'security/student_registration_security.xml',
        # 'security/ir.model.access.csv',
        # 'views/student_registration_views.xml',
        # 'views/student_profile_views.xml',
        # 'views/templates.xml',
        # 'data/student_registration_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'assets': {
        'web.assets_frontend': [
            'student_registration/static/src/js/student_registration_form.js',
            'student_registration/static/src/css/student_registration_form.css',
        ],
    },
}