from odoo import models, fields

class Paciente(models.Model):
    _name = 'modulo_hospital.paciente'
    _description = 'Paciente'

    id_paciente = fields.Char(string = "ID Paciente", required = True)
    nombre = fields.Char(string = "Nombre", required = True)
    apellidos = fields.Char(string = "Apellidos", required = True)
    sintomas = fields.Text(string = "Síntomas")
    diagnostico_ids = fields.One2many('modulo_hospital.diagnostico', 'paciente_id', string = "Diagnósticos")
    medico_ids = fields.Many2many('modulo_hospital.medico', compute='_compute_medicos', string="Médicos que atendieron al paciente")

    def _compute_medicos(self):
        for paciente in self:
            paciente.medico_ids = paciente.diagnostico_ids.mapped('medico_id')

