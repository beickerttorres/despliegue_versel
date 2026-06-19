from django.contrib import admin
from .models import Proyecto

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'estado', 'creado_por', 'fecha_inicio', 'fecha_fin']
    list_filter = ['estado']
    search_fields = ['nombre', 'descripcion']
    filter_horizontal = ['miembros']
