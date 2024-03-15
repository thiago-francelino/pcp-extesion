from odoo import fields, models


class ProductionRequest(models.Model):
    _name = 'production.request'

    name = fields.Char()

    def name_get(self):
        result = []
        for record in self:
            rec_name = "SOLICITAÇÃO DE PRODUÇÃO N°%s" % record.id
            result.append((record.id, rec_name))
            self.name = str(rec_name)
        return result

    _rec_name = 'name'

    project_info_ids = fields.One2many('project.info','production_request_id', string="Requisição")
    logged_in_user_id = fields.Many2one('res.users',string="Usuario de abertura", default=lambda self: self.env.user.id, readonly=True)
