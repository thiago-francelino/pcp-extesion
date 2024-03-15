from odoo import fields, models


class ArquiveCuttingPlan(models.Model):

    _name = 'arquive.cutting.plan'

    name = fields.Char()

    def name_get(self):
        result = []
        for record in self:
            rec_name = "DOCUMENTO N°%s" % record.id
            result.append((record.id, rec_name))
            self.name = str(rec_name)
        return result

    _rec_name = 'name'

    pdf_file = fields.Binary(string='Arquivo PDF', attachment=True)

