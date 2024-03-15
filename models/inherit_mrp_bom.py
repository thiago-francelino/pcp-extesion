from odoo import fields, models, api


class MrpBomExtension(models.Model):
    _inherit = 'mrp.bom'

    product_id = fields.Many2one('product.product', string="Produto", domain="[]", required=True)
    operation_ids = fields.Many2many('mrp.routing.workcenter', copy=True)

    @api.onchange('product_id')
    def onchance_product_id(self):
        if self.product_id:
            self.product_tmpl_id = self.product_id.product_tmpl_id

    @api.onchange('product_tmpl_id')
    def _onchange_product_id(self):
        if self.product_tmpl_id and self.product_tmpl_id.categ_id:
            self.operation_ids = [(6, 0, self.product_tmpl_id.categ_id.order_service_ids.ids)]
