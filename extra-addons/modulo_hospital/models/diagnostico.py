from odoo import models, fields

class Diagnostico(models.Model):
    _name = 'modulo_hospital.diagnostico'
    _description = 'Diagnósticos de los pacientes'

    medico_id = fields.Many2one('modulo_hospital.medico', string = 'Medico', required = True)
    paciente_id = fields.Many2one('modulo_hospital.paciente', string = 'Paciente', required = True)
    sintoma = fields.Text(related = 'paciente_id.sintomas', string = 'Sintomas', readonly = True)
    consulta = fields.Text(related = 'medico_id.consulta', string = 'Consultas', readonly = True)