from django.contrib import admin
from .models import Tarea

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'proyecto', 'asignado_a', 'estado', 'prioridad', 'fecha_limite']
    list_filter = ['estado', 'prioridad', 'proyecto']
    search_fields = ['titulo', 'descripcion']
