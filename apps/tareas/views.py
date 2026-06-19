from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.proyectos.models import Proyecto
from .models import Tarea
from .forms import TareaForm


@login_required
def lista_tareas(request):
    estado = request.GET.get('estado', '')
    prioridad = request.GET.get('prioridad', '')

    tareas = Tarea.objects.filter(asignado_a=request.user)

    if estado:
        tareas = tareas.filter(estado=estado)
    if prioridad:
        tareas = tareas.filter(prioridad=prioridad)

    return render(request, 'tareas/lista.html', {
        'tareas': tareas,
        'estados': Tarea.ESTADO_CHOICES,
        'prioridades': Tarea.PRIORIDAD_CHOICES,
        'estado_filtro': estado,
        'prioridad_filtro': prioridad,
    })


@login_required
def crear_tarea(request, proyecto_pk):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_pk)
    if request.method == 'POST':
        form = TareaForm(request.POST, proyecto=proyecto)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.proyecto = proyecto
            tarea.creado_por = request.user
            tarea.save()
            messages.success(request, f'Tarea "{tarea.titulo}" creada correctamente.')
            return redirect('detalle_proyecto', pk=proyecto.pk)
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = TareaForm(proyecto=proyecto)
    return render(request, 'tareas/crear.html', {'form': form, 'proyecto': proyecto})


@login_required
def editar_tarea(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    proyecto = tarea.proyecto
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea, proyecto=proyecto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarea actualizada correctamente.')
            return redirect('detalle_proyecto', pk=proyecto.pk)
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = TareaForm(instance=tarea, proyecto=proyecto)
    return render(request, 'tareas/editar.html', {'form': form, 'tarea': tarea, 'proyecto': proyecto})


@login_required
def eliminar_tarea(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    proyecto = tarea.proyecto
    if request.method == 'POST':
        titulo = tarea.titulo
        tarea.delete()
        messages.success(request, f'Tarea "{titulo}" eliminada.')
        return redirect('detalle_proyecto', pk=proyecto.pk)
    return render(request, 'tareas/confirmar_eliminar.html', {'tarea': tarea})


@login_required
def cambiar_estado(request, pk):
    """Cambio rápido de estado via POST desde la vista de detalle."""
    tarea = get_object_or_404(Tarea, pk=pk)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        estados_validos = [e[0] for e in Tarea.ESTADO_CHOICES]
        if nuevo_estado in estados_validos:
            tarea.estado = nuevo_estado
            tarea.save()
            messages.success(request, f'Estado actualizado a "{tarea.get_estado_display()}".')
    return redirect('detalle_proyecto', pk=tarea.proyecto.pk)
