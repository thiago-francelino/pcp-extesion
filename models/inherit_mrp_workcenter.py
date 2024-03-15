from odoo import fields, models, api


class InheritWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    department_id = fields.Many2one('hr.department', string="Departamento")
    
class InheritRoutingWorkcenter(models.Model):
    _inherit = 'mrp.routing.workcenter'
    product_category_id = fields.Many2one(
        'product.category',
        string='Product Category',
        required=True
    )
