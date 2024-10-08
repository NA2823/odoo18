{
    'name': 'Product Rent',
    'version': '18.0.1.0',
    'author': 'Elvyana',
    'license': 'LGPL-3',
    'description': 'Product rent and manufactring Management ERP System using odoo version 18.0',
    'summary': 'Product rent and manufactring Management ERP System using odoo version 18.0',
    'depends': [
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/product_readonly_views.xml',
        'views/customer_corner_views.xml',
        'views/booking_product_views.xml',
    ],
}