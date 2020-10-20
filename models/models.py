from odoo import models, fields, api


class Package(models.Model):
    _name = 'abbybee.package'
    _description = 'Contains package data'


    weight = fields.Float(required=True, string="Weight")