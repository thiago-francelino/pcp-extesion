from odoo import fields, models


class Material(models.Model):
    _name = 'material.and.occurrence'

    mrp_production_id = fields.Many2one('mrp.production', string="Ordem de Produção")


    # table