from odoo import fields, models, api


class PlanCut(models.Model):
    _name = 'cutting.plan'

    name = fields.Char()

    def name_get(self):
        result = []
        for record in self:
            rec_name = "PLANO DE CORTE N°%s" % record.id
            result.append((record.id, rec_name))
            self.name = str(rec_name)
        return result

    _rec_name = 'name'

    status = fields.Selection([('opened', 'Em aberto'), ('in progress', 'Em andamento'), ('finished', 'Finalizado')])
    project_info_ids = fields.One2many('project.info', 'cutting_plan_id',
                                                      string="Requisição")

    # os campos a seguir servem somente pra isualização na tree
    production_request_related = fields.Many2one(related="project_info_ids.production_request_id")
    feedstock_product_related = fields.Many2one(related="project_info_ids.feedstock_product_id")

    production_request_id = fields.Many2many('production.request')

    @api.onchange('production_request_id')
    def _onchange_production_request_id(self):
        if self.production_request_id:
            self.project_info_ids = [(5, 0, 0)]
            for project_info_id in self.production_request_id.project_info_ids:
                self.write({"project_info_ids": [[4, project_info_id.id,0]]})
        else:
            self.project_info_ids = [(5, 0, 0)]