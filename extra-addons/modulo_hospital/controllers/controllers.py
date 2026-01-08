# -*- coding: utf-8 -*-
# from odoo import http


# class ModuloHospital(http.Controller):
#     @http.route('/modulo_hospital/modulo_hospital', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/modulo_hospital/modulo_hospital/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('modulo_hospital.listing', {
#             'root': '/modulo_hospital/modulo_hospital',
#             'objects': http.request.env['modulo_hospital.modulo_hospital'].search([]),
#         })

#     @http.route('/modulo_hospital/modulo_hospital/objects/<model("modulo_hospital.modulo_hospital"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('modulo_hospital.object', {
#             'object': obj
#         })

