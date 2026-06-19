from django import forms
from django.contrib.auth.models import User
from .models import Tarea


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'asignado_a', 'estado', 'prioridad', 'fecha_limite']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la tarea'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción (opcional)'}),
            'asignado_a': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
            'fecha_limite': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'asignado_a': 'Asignar a',
            'estado': 'Estado',
            'prioridad': 'Prioridad',
            'fecha_limite': 'Fecha límite',
        }

    def __init__(self, *args, proyecto=None, **kwargs):
        super().__init__(*args, **kwargs)
        if proyecto:
            miembros_ids = list(proyecto.miembros.values_list('id', flat=True))
            miembros_ids.append(proyecto.creado_por.id)
            self.fields['asignado_a'].queryset = User.objects.filter(id__in=miembros_ids)
