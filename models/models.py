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
    date_sent = fields.Date(required=True, string="Date Sent")
    customer_id = fields.Many2one('abbybee.customer', required=True, string="Customer")

    @api.model
    def create(self, vals):
        new_value = vals['control_no']
        existing_records = self.env['abbybee.package'].search([('control_no', '=', new_value)])
        if len(existing_records) >= 1:
            raise ValidationError('Control Number value must be unique')
        result = super(Package, self).create(vals)
        return result

    def write(self, vals):
        try:
            new_value = vals['control_no']
        except:
            new_value = None

        if self.control_no == new_value:
            result = super(Package, self).write(vals)
            return result

        if new_value:
            existing_records = self.env['abbybee.package'].search([('control_no', '=', new_value)])
            if len(existing_records) >= 1:
                raise ValidationError('Control Number value must be unique')
        result = super(Package, self).write(vals)
        return result


class Customer(models.Model):
    _name = 'abbybee.customer'
    _description = 'Contains customers'

    # def name_get(self):
    #     result = []
    #     for record in self:
    #         result.append((record.id, record.control_no))
    #     return result

    customer_id = fields.Char(required=True, string="Customer ID")
    name = fields.Char(required=True, string="Name")
    address = fields.Char(required=True, string="Address")
    phone = fields.Char(required=True, string="Phone")


    @api.model
    def create(self, vals):
        new_value = vals['customer_id']
        existing_records = self.env['abbybee.customer'].search([('customer_id', '=', new_value)])
        if len(existing_records) >= 1:
            raise ValidationError('Customer ID value must be unique')
        result = super(Customer, self).create(vals)
        return result

    def write(self, vals):
        try:
            new_value = vals['customer_id']
        except:
            new_value = None

        if self.customer_id == new_value:
            result = super(Customer, self).write(vals)
            return result

        if new_value:
            existing_records = self.env['abbybee.customer'].search([('customer_id', '=', new_value)])
            if len(existing_records) >= 1:
                raise ValidationError('Customer ID value must be unique')
        result = super(Customer, self).write(vals)
        return result