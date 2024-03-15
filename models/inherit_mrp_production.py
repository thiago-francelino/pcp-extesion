import datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class InheritMrpProduction(models.Model):
    _inherit = "mrp.production"

    product_id = fields.Many2one(
        'product.product', 'Product',
        domain="""[('type', 'in', ['product']),'|',
                    ('company_id', '=', False),
                    ('company_id', '=', company_id)]""",
        readonly=True, required=True, check_company=True,
        states={'draft': [('readonly', False)]})

    @api.onchange('workorder_ids')
    def fill_operation_input(self):
        last_input = 0.0
        if self.workorder_ids:
            for index, line in enumerate(self.workorder_ids):
                if index == 0:
                    line.input_material = self.project_info_ids
                    last_input = line.output_material
                else:
                    line.input_material = last_input
                    last_input = line.output_material

    @api.onchange('workorder_ids')
    def parts_validation(self):
        last_input = 0.0
        if self.workorder_ids:
            for index, line in enumerate(self.workorder_ids):
                if index == 0:  # Verificação para primeira iteração
                    if line.input_material > self.product_qty:
                        # Impedir que o usuário coloque quantidade de entrada maior que a quantidade a ser produzida
                        raise UserError(_("Quantidade de entrada não pode ser maior que a quantidade a ser produzida!"))
                    if line.output_material > line.input_material:
                        # Impedir que o usuário coloque quantidade de saída maior que a de entrada
                        raise UserError(_("Quantidade de saída não pode ser maior que a quantidade de entrada"))
                    else:
                        last_input = line.output_material
                else:  # Próximas iterações
                    if line.input_material > last_input:
                        raise UserError(_("Quantidade de entrada não pode ser maior que a saída da operação anterior!"))
                    if line.output_material > line.input_material:
                        raise UserError(_("Quantidade de saída não pode ser maior que a quantidade de entrada"))
                    else:
                        last_input = line.output_material

    def button_mark_done(self):
        list_memory = []
        last_workorder = self.workorder_ids[-1] if self.workorder_ids else False
        if last_workorder.output_material < self.product_qty:
            res = super(InheritMrpProduction, self).button_mark_done()
            for rec in self.workorder_ids:
                list_memory.append([rec.input_material, rec.output_material])
                if rec.input_material > rec.output_material:
                    vals_stock_move = {
                        'product_id': rec.product_id.id,
                        'name': 'WH/MO/' + str(self.env['stock.move'].search([], limit=1, order='id desc').id + 1),
                        'date': datetime.datetime.now(),
                        'product_uom_qty': rec.input_material - rec.output_material,
                        'state': 'done',
                        'location_id': self.env['stock.location'].search([('complete_name', '=', 'WH/Stock')]).id,
                        'location_dest_id': self.env['stock.location'].search(
                            [('complete_name', '=', 'Virtual Locations/Scrap')]).id,
                        'product_uom': self.env['uom.uom'].search([('id', '=', self.env['product.template'].search(
                            [('id', '=', rec.product_id.product_tmpl_id.id)]).uom_id.id)]).id,
                    }
                    move_id = self.env['stock.move'].create(vals_stock_move)

                    vals_stock_move_line = {
                        'product_id': rec.product_id.id,
                        'date': datetime.datetime.now(),
                        'qty_done': rec.input_material - rec.output_material,
                        'move_id': move_id.id,
                        'reference': 'WH/MO/' + str(self.env['stock.move.line'].search([], limit=1, order='id desc').id + 1),
                        'state': 'done',
                        'location_id': self.env['stock.location'].search(
                            [('complete_name', '=', 'WH/Stock')]).id,
                        'location_dest_id': self.env['stock.location'].search(
                            [('complete_name', '=', 'Virtual Locations/Scrap')]).id,
                        'product_uom_id': self.env['uom.uom'].search([('id', '=', self.env['product.template'].search(
                            [('id', '=', rec.product_id.product_tmpl_id.id)]).uom_id.id)]).id,
                    }
                    self.env['stock.move.line'].create(vals_stock_move_line)

                    vals = {
                        'product_id': rec.product_id.id,
                        'name': 'SP' + str((self.env['stock.scrap'].search([], limit=1, order='id desc').id + 1)),
                        'date_done': datetime.datetime.now(),
                        'scrap_qty': rec.input_material - rec.output_material,
                        'product_uom_id': 1,
                        'production_id': str(self.id),
                        'state': 'done',
                        'origin': """Durante a ordem de serviço """ + str(rec.name) +  """ocorreu um problema e a peça foi descartada."""  
                        """OBSERVAÇÃO DO FUNCIONARIO: """ + str(rec.occurrence),
                    }
                    self.env['stock.scrap'].create(vals)
            for rec in range(len(list_memory)):
                if rec + 1 < len(list_memory):
                    if list_memory[rec][1] != list_memory[rec+1][0]:
                        vals_stock_move = {
                            'product_id': self.workorder_ids[rec].product_id.id,
                            'name': 'WH/MO/' + str(self.env['stock.move'].search([], limit=1, order='id desc').id + 1),
                            'date': datetime.datetime.now(),
                            'product_uom_qty': list_memory[rec][1] - list_memory[rec+1][0],
                            'state': 'done',
                            'location_id': self.env['stock.location'].search([('complete_name', '=', 'WH/Stock')]).id,
                            'location_dest_id': self.env['stock.location'].search(
                                [('complete_name', '=', 'Virtual Locations/Scrap')]).id,
                            'product_uom': self.env['uom.uom'].search([('id', '=', self.env['product.template'].search(
                                [('id', '=', self.workorder_ids[rec].product_id.product_tmpl_id.id)]).uom_id.id)]).id,
                        }
                        move_id = self.env['stock.move'].create(vals_stock_move)

                        vals_stock_move_line = {
                            'product_id': self.workorder_ids[rec].product_id.id,
                            'date': datetime.datetime.now(),
                            'qty_done': list_memory[rec][1] - list_memory[rec+1][0],
                            'move_id': move_id.id,
                            'reference': 'WH/MO/' + str(
                                self.env['stock.move.line'].search([], limit=1, order='id desc').id + 1),
                            'state': 'done',
                            'location_id': self.env['stock.location'].search(
                                [('complete_name', '=', 'WH/Stock')]).id,
                            'location_dest_id': self.env['stock.location'].search(
                                [('complete_name', '=', 'Virtual Locations/Scrap')]).id,
                            'product_uom_id': self.env['uom.uom'].search([('id', '=', self.env['product.template'].search(
                                [('id', '=', self.workorder_ids[rec].product_id.product_tmpl_id.id)]).uom_id.id)]).id,
                        }
                        self.env['stock.move.line'].create(vals_stock_move_line)

                        vals = {
                            'product_id': self.workorder_ids[rec].product_id.id,
                            'name': 'SP' + str((self.env['stock.scrap'].search([], limit=1, order='id desc').id + 1)),
                            'date_done': datetime.datetime.now(),
                            'scrap_qty': list_memory[rec][1] - list_memory[rec+1][0],
                            'product_uom_id': 1,
                            'production_id': str(self.id),
                            'state': 'done',
                            'origin': 'Entre a ' + str(rec+1) + '° e a '+str(rec+2)+ '° ordem de serviço ocorreu um problema e a peça foi descartada.',
                        }
                        self.env['stock.scrap'].create(vals)
        else:
            res = super(InheritMrpProduction, self).button_mark_done()
