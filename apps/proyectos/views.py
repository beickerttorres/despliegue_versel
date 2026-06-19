from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Proyecto
from .forms import ProyectoForm
from apps.tareas.models import Tarea


@login_required
def dashboard(request):
    proyectos = Proyecto.objects.filter(
        Q(creado_por=request.user) | Q(miembros=request.user)
    ).distinct()

    mis_tareas = Tarea.objects.filter(
        asignado_a=request.user
    ).exclude(estado='completada').order_by('fecha_limite')[:5]

    context = {
        'total_proyectos': proyectos.count(),
        'proyectos_activos': proyectos.filter(estado='activo').count(),
        'total_tareas': Tarea.objects.filter(
            Q(proyecto__creado_por=request.user) | Q(asignado_a=request.user)
        ).distinct().count(),
        'tareas_pendientes': Tarea.objects.filter(
            asignado_a=request.user, estado='pendiente'
        ).count(),
        'tareas_en_progreso': Tarea.objects.filter(
            asignado_a=request.user, estado='en_progreso'
        ).count(),
        'tareas_completadas': Tarea.objects.filter(
            asignado_a=request.user, estado='completada'
        ).count(),
        'proyectos_recientes': proyectos[:4],
        'mis_tareas': mis_tareas,
    }
    return render(request, 'dashboard.html', context)


@login_required
def lista_proyectos(request):
    q = request.GET.get('q', '')
    estado = request.GET.get('estado', '')

    proyectos = Proyecto.objects.filter(
        Q(creado_por=request.user) | Q(miembros=request.user)
    ).distinct()

    if q:
        proyectos = proyectos.filter(nombre__icontains=q)
    if estado:
        proyectos = proyectos.filter(estado=estado)

    return render(request, 'proyectos/lista.html', {
        'proyectos': proyectos,
        'q': q,
        'estado_filtro': estado,
        'estados': Proyecto.ESTADO_CHOICES,
    })


@login_required
def detalle_proyecto(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    tareas = proyecto.tareas.all().order_by('estado', '-creado_en')
    return render(request, 'proyectos/detalle.html', {
        'proyecto': proyecto,
        'tareas': tareas,
    })


@login_required
def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.creado_por = request.user
            proyecto.save()
            form.save_m2m()
            messages.success(request, f'Proyecto "{proyecto.nombre}" creado correctamente.')
            return redirect('detalle_proyecto', pk=proyecto.pk)
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = ProyectoForm()
    return render(request, 'proyectos/crear.html', {'form': form})


@login_required
def editar_proyecto(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk, creado_por=request.user)
    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proyecto actualizado correctamente.')
            return redirect('detalle_proyecto', pk=proyecto.pk)
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = ProyectoForm(instance=proyecto)
    return render(request, 'proyectos/editar.html', {'form': form, 'proyecto': proyecto})


@login_required
def eliminar_proyecto(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk, creado_por=request.user)
    if request.method == 'POST':
        nombre = proyecto.nombre
        proyecto.delete()
        messages.success(request, f'Proyecto "{nombre}" eliminado.')
        return redirect('lista_proyectos')
    return render(request, 'proyectos/confirmar_eliminar.html', {'proyecto': proyecto})
