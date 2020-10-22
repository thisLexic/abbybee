from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)


class Package(models.Model):
    _name = 'abbybee.package'
    _description = 'Contains package data'

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.control_no))
        return result

    @api.depends('weight')
    def _get_cost(self):
        for rec in self:
            rec.cost = rec.weight * 5


    control_no = fields.Char(required=True, string="Control Number")
    weight = fields.Float(required=True, string="Weight")
    date_sent = fields.Date(required=True, string="Date Sent")
    customer_id = fields.Many2one('abbybee.customer', required=True, string="Customer")
    service_id = fields.Many2one('abbybee.service', required=True, string="Service")
    date_received = fields.Date(string="Date Received")
    recipient_signature = fields.Binary(string="Recipient Signature")
    delivery_id = fields.Many2one('abbybee.delivery', string="Delivery Staff")
    recipient_id = fields.Many2one('abbybee.recipient', string="Recipient")
    cost = fields.Float(compute='_get_cost', string="Cost")

    @api.model
    def create(self, vals):
        new_value = vals['control_no']
        existing_records = self.env['abbybee.package'].search([('control_no', '=', new_value)])
        if len(existing_records) >= 1:
            raise ValidationError('Control Number value must be unique')

        date_rec = vals['date_received']
        rec_sign = vals['recipient_signature']
        deli_id = vals['delivery_id']
        rec_id = vals['recipient_id']

        if date_rec and rec_sign and deli_id and rec_id:
            result = super(Package, self).create(vals)
            return result
        elif not(date_rec) and not(rec_sign) and not(deli_id) and not(rec_id):
            result = super(Package, self).create(vals)
            return result
        else:
            raise ValidationError('If a field under Receipt has a value, all fields must have a value')


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

        date_rec = 'date_received' in vals
        rec_sign = 'recipient_signature' in vals
        deli_id = 'delivery_id' in vals
        rec_id = 'recipient_id' in vals

        if rec_sign:
            if vals['recipient_signature']:
                pass
            else:
                rec_sign = False

        # if date_rec != rec_sign or date_rec != deli_id or rec_sign != deli_id or rec_id != date_rec or rec_id != rec_sign or rec_id != deli_id:
            # raise ValidationError('If a field under Receipt has a value, all fields must have a value')

        if date_rec and rec_sign and deli_id and rec_id:
            result = super(Package, self).write(vals)
            return result
        elif not(date_rec) and not(rec_sign) and not(deli_id) and not(rec_id):
            result = super(Package, self).write(vals)
            return result
        else:
            raise ValidationError('If a field under Receipt has a value, all fields must have a value')



class Customer(models.Model):
    _name = 'abbybee.customer'
    _description = 'Contains customers'

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.name))
        return result

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

class Service(models.Model):
    _name = 'abbybee.service'
    _description = 'Contains services'

    def name_get(self):
        result = []
        for record in self:
            name = record.service_type + " " + record.package_type + ": O - " + record.origin_area + " D - " + record.destination_area
            result.append((record.id, name))
        return result

    service_id = fields.Char(required=True, string="Service ID")
    delivery_time = fields.Selection([('next', 'Next Day'), ('3to4days', '3 - 4 Days')], required=True, string="Delivery time")
    service_type = fields.Selection([('express', 'Express'), ('ordinary', 'Ordinary')], required=True, string="Service Type")
    package_type = fields.Selection([('letter', 'Letter'), ('package', 'Package'), ('parcel', 'Parcel'), ('box', 'Box')], required=True, string="Package Type")
    destination_area = fields.Selection([('luzon', 'Luzon'), ('visayas', 'Visayas'), ('mindanao', 'Mindanao')], required=True, string="Destination Area")
    origin_area = fields.Selection([('luzon', 'Luzon'), ('visayas', 'Visayas'), ('mindanao', 'Mindanao')], required=True, string="Origin Area")



    @api.model
    def create(self, vals):
        new_value = vals['service_id']
        existing_records = self.env['abbybee.service'].search([('service_id', '=', new_value)])
        if len(existing_records) >= 1:
            raise ValidationError('Service ID value must be unique')
        result = super(Service, self).create(vals)
        return result

    def write(self, vals):
        try:
            new_value = vals['service_id']
        except:
            new_value = None

        if self.service_id == new_value:
            result = super(Service, self).write(vals)
            return result

        if new_value:
            existing_records = self.env['abbybee.service'].search([('service_id', '=', new_value)])
            if len(existing_records) >= 1:
                raise ValidationError('Service ID value must be unique')
        result = super(Service, self).write(vals)
        return result

class Delivery(models.Model):
    _name = 'abbybee.delivery'
    _description = 'Contains delivery staff'

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.name))
        return result

    courier_id = fields.Char(required=True, string="Delivery Staff ID")
    name = fields.Char(required=True, string="Name")


    @api.model
    def create(self, vals):
        new_value = vals['courier_id']
        existing_records = self.env['abbybee.delivery'].search([('courier_id', '=', new_value)])
        if len(existing_records) >= 1:
            raise ValidationError('Delivery Staff ID value must be unique')
        result = super(Delivery, self).create(vals)
        return result

    def write(self, vals):
        try:
            new_value = vals['courier_id']
        except:
            new_value = None

        if self.courier_id == new_value:
            result = super(Delivery, self).write(vals)
            return result

        if new_value:
            existing_records = self.env['abbybee.delivery'].search([('courier_id', '=', new_value)])
            if len(existing_records) >= 1:
                raise ValidationError('Delivery Staff ID value must be unique')
        result = super(Delivery, self).write(vals)
        return result

class Recipient(models.Model):
    _name = 'abbybee.recipient'
    _description = 'Contains recipients'

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.name))
        return result

    recipient_id = fields.Char(required=True, string="Recipient ID")
    name = fields.Char(required=True, string="Name")
    address = fields.Char(required=True, string="Address")
    phone = fields.Char(required=True, string="Phone")


    @api.model
    def create(self, vals):
        new_value = vals['recipient_id']
        existing_records = self.env['abbybee.recipient'].search([('recipient_id', '=', new_value)])
        if len(existing_records) >= 1:
            raise ValidationError('Recipient ID value must be unique')
        result = super(Recipient, self).create(vals)
        return result

    def write(self, vals):
        try:
            new_value = vals['recipient_id']
        except:
            new_value = None

        if self.recipient_id == new_value:
            result = super(Recipient, self).write(vals)
            return result

        if new_value:
            existing_records = self.env['abbybee.recipient'].search([('recipient_id', '=', new_value)])
            if len(existing_records) >= 1:
                raise ValidationError('Recipient ID value must be unique')
        result = super(Recipient, self).write(vals)
        return result
