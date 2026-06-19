from django.db import models
from django.contrib.auth.models import User


class Proyecto(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('pausado', 'Pausado'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]

    nombre = models.CharField(max_length=200, verbose_name='Nombre del proyecto')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo', verbose_name='Estado')
    fecha_inicio = models.DateField(verbose_name='Fecha de inicio')
    fecha_fin = models.DateField(null=True, blank=True, verbose_name='Fecha de entrega')
    creado_por = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='proyectos_creados', verbose_name='Creado por'
    )
    miembros = models.ManyToManyField(
        User, related_name='proyectos_miembro',
        blank=True, verbose_name='Miembros'
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    def total_tareas(self):
        return self.tareas.count()

    def tareas_completadas(self):
        return self.tareas.filter(estado='completada').count()

    def porcentaje_avance(self):
        total = self.total_tareas()
        if total == 0:
            return 0
        return int((self.tareas_completadas() / total) * 100)

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ['-creado_en']
