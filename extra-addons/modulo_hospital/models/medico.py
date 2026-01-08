from odoo import models, fields

class Medico(models.Model):
    _name = 'modulo_hospital.medico'
    _description = 'Medico'

    id_medico = fields.Char(string = "ID Medico", required = True)
    nombre = fields.Char(string = "Nombre", required = True)
    apellidos = fields.Char(string = "Apellidos", required = True)
    numero_colegiado = fields.Char(string = "Nª colegiado", required = True)



    id_paciente = fields.Char(string="ID Paciente", required=True)
    nombre = fields.Char(string="Nombre", required=True)
    apellidos = fields.Char(string="Apellidos", required=True)
    sintomas = fields.Text(string="Síntomas")
    diagnostico_id = fields.One2Many('modulo_hospital.diagnostico', 'diagnostico_id', string="Diagnósticos")
    medico_ids = fields.Many2Many('modulo_hospital.medico', compute='_compute_medicos',
                                  string="Médicos que atendieron al paciente")

    def _compute_medicos(self):
        for paciente in self:
            paciente.medico_ids = paciente.diagnostico_id.mapped('medico_id')