from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Package(models.Model):
    _name = 'abbybee.package'
    _description = 'Contains package data'

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.control_no))
        return result


    control_no = fields.Char(required=True, string="Control Number")
    weight = fields.Float(required=True, string="Weight")

    @api.model
    def create(self, vals):
        new_value = vals['control_no']
        existing_records = self.env['abbybee.package'].search([('control_no', '=', new_value)])
        if len(existing_records) >= 1:
            raise ValidationError('Control Number value must be unique')
        result = super(Package, self).create(vals)
        return result

    def write(self, vals):
        new_value = vals['control_no']
        existing_records = self.env['abbybee.package'].search([('control_no', '=', new_value)])
        if len(existing_records) >= 1:
            raise ValidationError('Control Number value must be unique')
        result = super(Package, self).write(vals)
        return result