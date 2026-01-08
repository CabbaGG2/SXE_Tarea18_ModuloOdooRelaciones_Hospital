# -*- coding: utf-8 -*-

from odoo import models, fields

class Estudiante(models.Model):
    _name = "fp_management.estudiante"
    _description = "Estudiante de FP"
    _order = "name asc"

    name = fields.Char(string="Nombre del Estudiante", required=True)
    edad = fields.Integer(string="Edad")
    ciclo_id = fields.Many2one("fp_management.ciclo", string="Ciclo Formativo", required=True)
    
    via_acceso = fields.Selection(
        [
            ("eso", "ESO"),
            ("ciclo_medio", "Ciclo Medio"),
            ("bachillerato", "Bachillerato"),
            ("prueba_acceso", "Prueba de Acceso"),
            ("otros", "Otros"),
        ],
        string="Vía de Acceso",
        required=True,
        default="eso",
    )
