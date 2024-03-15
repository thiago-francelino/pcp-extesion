from odoo import fields, models, api


class MOExtension(models.Model):
    _name = 'mo.extension'

    mrp_production_id = fields.Many2one('mrp.production', string="Ordem de Produção")
    workorder_ids = fields.One2many("mrp.workorder", "mo_extension_id", compute="compute_workorder_ids", store=True)

    @api.depends('mrp_production_id')
    def compute_workorder_ids(self):
        if self.workorder_ids:
            self.workorder_ids.unlink()
        if self.mrp_production_id:
            user = self.env.user
            workcenter_ids = self.env['mrp.workcenter'].search([('department_id','=',user.department_id.id)])
            self.workorder_ids = self.env['mrp.workorder'].search([('workcenter_id','in',workcenter_ids.ids),
                                                                   ('production_id','=',self.mrp_production_id.id)])
        else:
            self.workorder_ids = False