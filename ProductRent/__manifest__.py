{
    'name': 'Product Rent',
    'version': '18.0.1.0',
    'author': 'Elvyana',
    'license': 'LGPL-3',
    'description': 'Product rent and manufacturing Management ERP System using odoo version 18.0',
    'summary': 'Product rent and manufacturing Management ERP System using odoo version 18.0',
    'depends': [
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/product_views.xml',
        'views/product_readonly_views.xml',
        'views/customer_corner_views.xml',
        'views/booking_product_views.xml',
        'views/finance_corner_views.xml',
        'report/product_booking_report.xml',
    ],
}