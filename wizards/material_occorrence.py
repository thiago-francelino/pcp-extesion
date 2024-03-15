from odoo import fields, models


class MaterialOccorrence(models.TransientModel):
    _name = 'material.occurrence'

    material_output = fields.Integer("Saída de Peças")
    occurrence = fields.Text("Ocorrência")
    workorder_id = fields.Many2one('mrp.workorder')

    def send(self):
        self.workorder_id.write({"output_material": self.material_output,
                                 "occurrence": self.occurrence})
        next_work_order_id = self.env['mrp.workorder'].search([('id','=',(self.workorder_id.id+1)),('production_id','=',self.workorder_id.production_id.id)])
        if next_work_order_id:
            next_work_order_id.write({"input_material": self.material_output})

