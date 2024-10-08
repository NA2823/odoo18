from odoo import api, models, fields, _
from odoo.exceptions import ValidationError, UserError


class ProductDetail(models.Model):
    _name = 'product.detail'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Product Detail'

    product_id = fields.Char(string="Product ID", default="New")
    product_name = fields.Char(string="Product Name", required=True, tracking=True)
    product_image = fields.Image(string="Product Image", required=True, tracking=True)
    category_id = fields.Many2one('products.category', string="Category", required=True, )
    subcategory_id = fields.Many2one('product.subcategory', string="Subcategory", required=True,
                                     domain="[('category_id', '=', category_id)]")
    currency_id = fields.Many2one('res.currency', string='Currency', default=20)
    product_rent_price = fields.Monetary(string="Rent Price", required=True, tracking=True)
    total_qty = fields.Integer(string="Total Quantity", default=1)
    product_detail = fields.Html(string="Product Detail")


class ProductsCategory(models.Model):
    _name = "products.category"
    _description = "Products Category"

    name = fields.Char(string="Category Name", required=True)

    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            if self.search_count([('name', '=', record.name)]) > 1:
                raise ValidationError(_("The Category Name must be unique."))


class ProductSubcategory(models.Model):
    _name = "product.subcategory"
    _description = "Product Subcategory"

    category_id = fields.Many2one('products.category', string='Category', required=True)
    name = fields.Char(string="Subcategory Name", required=True)

    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            if self.search_count([('name', '=', record.name)]) > 1:
                raise ValidationError(_("The Subcategory Name must be unique."))
