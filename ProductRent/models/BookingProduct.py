from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta


# Product Booking
# ================================>
class ProductBooking(models.Model):
    _name = "product.booking"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Product Booking"

    bill_number = fields.Char(string="Bill Number", default="New", readonly=True)
    billing_date = fields.Date(string="Billing Date", required=True, tracking=True, default=fields.Date.context_today)
    customer_id = fields.Many2one('customer.corner', string="Customer Name", required=True, tracking=True, )
    phone = fields.Char(string="Phone", related="customer_id.phone")
    email = fields.Char(string="Email", required=True, related="customer_id.email")
    address = fields.Text(string="Address", required=True, related="customer_id.address")
    booking_date = fields.Date(string="Booking Date", required=True, tracking=True, )
    return_date = fields.Date(string="Return Date", required=True, tracking=True, )
    currency_id = fields.Many2one('res.currency', string='Currency', default=20)
    booking_product_line_id = fields.One2many('product.booking.line', 'product_booking_id', string="Products")
    payable_amount = fields.Monetary(string="Payable Amount", compute="_compute_payable_amount", store=True, )
    note = fields.Text(string="Note")


    @api.constrains('booking_date')
    def _check_unique_and_valid_fields(self):
        for record in self:
            # Validate booking and return dates
            today = date.today()
            if record.booking_date and record.booking_date < today:
                raise ValidationError("Booking date cannot be in the past.")
            if record.return_date and record.return_date <= record.booking_date:
                raise ValidationError("Return date must be after the booking date.")

    @api.depends("booking_product_line_id")
    def _compute_payable_amount(self):
        for rec in self:
            rec.payable_amount = 0
            for i in rec.booking_product_line_id:
                rec.payable_amount += i.total_price


# Product Booking Line
# ================================>
class ProductBookingLine(models.Model):
    _name = "product.booking.line"
    _description = "Product Booking Line"

    product_ids = fields.Many2one('product.detail', string="Product", required=True)
    product_image = fields.Image(string="Product Image", related="product_ids.product_image")
    product_name = fields.Char(string="Product Name", related="product_ids.product_name")
    qty = fields.Integer(string="Quantity", default=1)
    price = fields.Monetary(string="Rent Price", related="product_ids.product_rent_price")
    product_booking_id = fields.Many2one('product.booking', string="Customer")
    currency_id = fields.Many2one('res.currency', string='Currency', default=20)
    discount_id = fields.Many2many  ('discount.tag', string="Discount")
    total_price = fields.Monetary(string="Total Price", compute="_compute_total", )

    @api.depends('qty', 'price', 'discount_id')
    def _compute_total(self):
        for rec in self:
            total = rec.qty * rec.price
            discount_percentage = rec.discount_id.percentage if rec.discount_id else 0
            total -= (total * discount_percentage / 100)

            rec.total_price = total


# Discount Tag
# ================================>
class DiscountTag(models.Model):
    _name = "discount.tag"
    _description = "Discount Tag"

    name = fields.Char(string="Name", required=True)
    percentage = fields.Float(string="Discount Percentage", required=True)
