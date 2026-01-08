# -*- coding: utf-8 -*-

from odoo import models, fields

class Ciclo(models.Model):
    _name = "fp_management.ciclo"
    _description = "Ciclo Formativo de FP"

    name = fields.Char(string="Nombre del Ciclo", required=True)
    descripcion = fields.Text(string="Descripción del ciclo formativo")
    estudiante_ids = fields.One2many("fp_management.estudiante", "ciclo_id", string="Estudiantes")
