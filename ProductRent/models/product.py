from odoo import api, models, fields, _
from odoo.exceptions import ValidationError, UserError
from datetime import date


class ProductDetail(models.Model):
    _name = 'product.detail'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Product Detail'

    name = fields.Char(string="Product ID", )
    product_name = fields.Char(string="Product Name", required=True, tracking=True)
    product_image = fields.Image(string="Product Image", required=True, tracking=True)
    category_id = fields.Many2one('products.category', string="Category", required=True, )
    subcategory_id = fields.Many2one('product.subcategory', string="Subcategory", required=True,
                                     domain="[('category_id', '=', category_id)]")
    currency_id = fields.Many2one('res.currency', string='Currency', default=20)
    product_rent_price = fields.Monetary(string="Rent Price", required=True, tracking=True)
    total_qty = fields.Integer(string="Total Quantity", default=1)
    product_detail = fields.Html(string="Product Detail")
    is_available = fields.Boolean(string="Is Available", default=True, compute="_compute_is_available"  )
    product_bill = fields.Many2many('product.booking', string="product Bill", compute="_compute_product_bill")

    @api.depends('product_bill')
    def _compute_product_bill(self):
        for rec in self:
            rec.product_bill = self.env['product.booking'].search(
                [('booking_product_line_id.product_ids', '=', rec.id)])

    @api.depends('product_bill')
    def _compute_is_available(self):
        for rec in self:
            today = date.today()
            is_booked = False
            for booking in rec.product_bill:
                if booking.booking_date <= today <= booking.return_date:
                    is_booked = True
                    break
            rec.is_available = not is_booked

    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            if self.search_count([('name', '=', record.name)]) > 1:
                raise ValidationError(_("The Product ID must be unique."))

            if len(self.product_name) > 40:
                raise ValidationError(
                    _(f"The Product Name max character 40 allow you enter {len(self.product_name)} character."))


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
