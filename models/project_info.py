from odoo import fields, models


class ProjectionInfo(models.Model):
    _name = 'project.info'

    name = fields.Char()

    def name_get(self):
        result = []
        for record in self:
            rec_name = str(record.product_id.product_tmpl_id.name) + " - " + str(record.project_info_ids) + " unidade(s)"
            result.append((record.id, rec_name))
            record.name = str(rec_name)
        return result

    _rec_name = 'name'

    product_id = fields.Many2one('product.product', string="Produto", required="1")
    product_qty = fields.Integer(string="Quantidade")
    production_request_id = fields.Many2one('production.request')
    cutting_plan_id = fields.Many2one('cutting.plan')
    feedstock_product_id = fields.Many2one('product.product', string="Produto materia prima", required="1")
    archive_pdf_cutting_plan_id = fields.Many2one('arquive.cutting.plan')
