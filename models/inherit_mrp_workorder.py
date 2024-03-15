from datetime import datetime
from odoo import fields, models


class MrpWorkorderExtension(models.Model):
    _inherit = 'mrp.workorder'

    input_material = fields.Integer(string="Ent. Peças")
    output_material = fields.Integer(string="Saída de peças")
    mo_extension_id = fields.Many2one("mo.extension")
    occurrence = fields.Text()

    def button_finish(self):
        end_date = datetime.now()
        for workorder in self:
            if workorder.state in ('done', 'cancel'):
                continue
            workorder.end_all()
            vals = {
                'qty_produced': workorder.qty_produced or workorder.qty_producing or workorder.qty_production,
                'state': 'done',
                'date_finished': end_date,
                'date_planned_finished': end_date
            }
            if not workorder.date_start:
                vals['date_start'] = end_date
            if not workorder.date_planned_start or end_date < workorder.date_planned_start:
                vals['date_planned_start'] = end_date
            workorder.with_context(bypass_duration_calculation=True).write(vals)

            workorder._start_nextworkorder()

        if len(self.ids) == 1:
            ctx = dict()
            ctx.update({
                'default_workorder_id': self.id
            })
            return {
                'type': 'ir.actions.act_window',
                'name': 'Saída de Peças',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'material.occurrence',
                'views': [[self.env.ref("pcp_extension.material_occurence_form_view").id, 'form']],
                'target': 'new',
                'context': ctx
            }
        else:
            return True