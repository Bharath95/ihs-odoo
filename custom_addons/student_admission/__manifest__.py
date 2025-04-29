# -*- coding: utf-8 -*-
{
    'name': "Student Admission Registration",

    'summary': """
        Module to handle student admission registrations submitted via API from a React frontend.""",

    'description': """
        - Creates a model 'student.registration' to store admission details.
        - Provides a JSON API endpoint '/student-registration/create' for data submission.
    """,

    'author': "Your Name / Company", # Change this
    'website': "https://www.yourcompany.com", # Change this

    'category': 'Education', # Or 'Uncategorized'
    'version': '18.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'], # 'web' is needed for controllers

    # always loaded
    'data': [
        'security/ir.model.access.csv', # Add later for security
        'views/student_admission_views.xml', # Add later for Odoo UI views
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True,
    'application': True, # Set to True if this is a standalone application
    'license': 'LGPL-3', # Or your chosen license
}