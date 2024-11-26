from django.db import models

# Create your models here.

class Evento(models.Model):
    TIPO_EVENTO = [
        ('inicio_semestre', 'Inicio de Semestre'),
        ('fin_semestre', 'Fin de Semestre'),
        ('inicio_inscripcion', 'Inicio de Inscripción de Asignaturas'),
        ('fin_inscripcion', 'Fin de Inscripción de Asignaturas'),
        ('receso_academico', 'Receso Académico'),
        ('feriado_nacional', 'Feriado Nacional'),
        ('feriado_regional', 'Feriado Regional'),
        ('inicio_solicitudes', 'Inicio de Plazos de Solicitudes Administrativas'),
        ('fin_solicitudes', 'Fin de Plazos de Solicitudes Administrativas'),
        ('inicio_beneficios', 'Inicio de Plazos para la Gestión de Beneficios'),
        ('fin_beneficios', 'Fin de Plazos para la Gestión de Beneficios'),
        ('ceremonia_titulacion', 'Ceremonia de Titulación o Graduación'),
        ('reunion_consejo', 'Reunión de Consejo Académico'),
        ('talleres_charlas', 'Talleres y Charlas'),
        ('dia_orientacion', 'Día de Orientación para Nuevos Estudiantes'),
        ('eventos_extracurriculares', 'Eventos Extracurriculares'),
        ('inicio_clases', 'Inicio de Clases'),
        ('ultimo_dia_clases', 'Último Día de Clases'),
        ('dia_puertas_abiertas', 'Día de Puertas Abiertas'),
        ('suspension_completa', 'Suspensión de Actividades Completa'),
        ('suspension_parcial', 'Suspensión de Actividades Parcial'),
        ('civil', 'Civil'),
    ]  
    nombre = models.CharField(max_length=100)  # Nombre del evento
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    comentarios = models.TextField(null=True, blank=True)  # Comentarios opcionales
    tipo = models.CharField(max_length=50, choices=TIPO_EVENTO)  # Tipo del evento

    class Meta:
        ordering = ['fecha_inicio']  # Orden ascendente por fecha_inicio

    def __str__(self):
        return f'{self.nombre} ({self.tipo})'


