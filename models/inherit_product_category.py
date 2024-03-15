
from odoo import models, fields, api

class ProductCategory(models.Model):
    _inherit = 'product.category'

    order_service_ids = fields.One2many(
        'mrp.routing.workcenter',
        'product_category_id',
        string='Order Services'
    )
