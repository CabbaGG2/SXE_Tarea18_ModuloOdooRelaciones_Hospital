# -*- coding: utf-8 -*-
# from odoo import http


# class FpManagement(http.Controller):
#     @http.route('/fp_management/fp_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fp_management/fp_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('fp_management.listing', {
#             'root': '/fp_management/fp_management',
#             'objects': http.request.env['fp_management.fp_management'].search([]),
#         })
#     @http.route('/fp_management/fp_management/objects/<model("fp_management.fp_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fp_management.object', {
#             'object': obj
#         })

