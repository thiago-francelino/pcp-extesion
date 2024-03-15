from odoo import models, fields, api

class InheritStockMove(models.Model):

    _inherit = "stock.move"

    product_id = fields.Many2one(
        'product.product', 'Product',
        domain="""[('type', 'in', ['consu']),'|',
                    ('company_id', '=', False),
                    ('company_id', '=', company_id)]""",
        readonly=True, required=True, check_company=True,
        states={'draft': [('readonly', False)]})