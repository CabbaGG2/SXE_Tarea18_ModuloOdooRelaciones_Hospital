from odoo import models, fields

class Medico(models.Model):
    _name = 'modulo_hospital.medico'
    _description = 'Medico'

    id_medico = fields.Char(string = "ID Medico", required = True)
    nombre = fields.Char(string = "Nombre", required = True)
    apellidos = fields.Char(string = "Apellidos", required = True)
    numero_colegiado = fields.Char(string = "Nª colegiado", required = True)
    consulta = fields.Text(string = "Consultas")
    diagnostico_ids = fields.One2many('modulo_hospital.diagnostico', 'medico_id', string = "Diagnósticos")
    paciente_ids = fields.Many2many('modulo_hospital.paciente', compute = '_compute_pacientes', string = 'Pacientes atendidos por este medico')

    def _compute_pacientes(self):
        for medico in self:
            medico.paciente_ids = medico.diagnostico_ids.mapped('paciente_id')
