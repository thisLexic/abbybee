# -*- coding: utf-8 -*-
# from odoo import http


# class Abbybee(http.Controller):
#     @http.route('/abbybee/abbybee/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/abbybee/abbybee/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('abbybee.listing', {
#             'root': '/abbybee/abbybee',
#             'objects': http.request.env['abbybee.abbybee'].search([]),
#         })

#     @http.route('/abbybee/abbybee/objects/<model("abbybee.abbybee"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('abbybee.object', {
#             'object': obj
#         })
