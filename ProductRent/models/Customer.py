from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
import re


# Customer Detail
#================================>
class CustomerCorner(models.Model):
    _name = "customer.corner"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Customer Detail"

    name = fields.Char(string="Customer Name", required=True, tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    reference_by = fields.Selection(
        [('instagram', 'Instagram'), ('friend', 'Friend'), ('relatives', 'Relatives'), ('other', 'Other')],
        string="Reference By")
    phone = fields.Char(string="Phone", required=True)
    email = fields.Char(string="Email", required=True)
    address = fields.Text(string="Address", required=True)
    booking_product_id = fields.One2many('product.booking', 'customer_id', string="Bookings")

    @api.constrains('phone', 'email', 'booking_date', )
    def _check_unique_and_valid_fields(self):
        for record in self:
            # Validate phone number and unique phone
            if record.phone:
                if not record.phone.isdigit() or len(record.phone) != 10:
                    raise ValidationError("Phone number must be exactly 10 digits long and contain only numbers.")

                phone_count = self.search_count([('phone', '=', record.phone), ('id', '!=', record.id)])
                if phone_count > 0:
                    raise ValidationError(f"Phone '{record.phone}' must be unique.")

            # Validate email format and unique email
            if record.email:
                email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_regex, record.email):
                    raise ValidationError("Email is not in a valid format.")

                email_count = self.search_count([('email', '=', record.email), ('id', '!=', record.id)])
                if email_count > 0:
                    raise ValidationError(f"Email '{record.email}' must be unique.")

