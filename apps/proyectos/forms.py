from django import forms
from django.contrib.auth.models import User
from .models import Proyecto


class ProyectoForm(forms.ModelForm):
    miembros = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Miembros del equipo'
    )

    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'estado', 'fecha_inicio', 'fecha_fin', 'miembros']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del proyecto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción del proyecto'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'estado': 'Estado',
            'fecha_inicio': 'Fecha de inicio',
            'fecha_fin': 'Fecha de entrega',
        }
