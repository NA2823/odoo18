from odoo import fields, models, api


class FinanceCorner(models.Model):
    _name = 'finance.corner'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Finance Corner'

    name = fields.Char(string="Finance Name", required=True, )
    date_of_create = fields.Date(string="Date", default=fields.Date.context_today)
    amount = fields.Monetary(string="Amount", required=True)
    currency_id = fields.Many2one('res.currency', string="Currency", required=True)
    finance_type = fields.Selection([('income', 'Income'), ('expense', 'Expense')], string="Finance Type",
                                    required=True, default="income")
    amount_in = fields.Selection([('cash', 'Cash'), ('upi', 'UPI')], string="Amount In")
    product_bill = fields.Many2one('product.booking', string="Product Bill")
    description = fields.Text(string="Description")

