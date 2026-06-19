from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_tareas, name='lista_tareas'),
    path('proyecto/<int:proyecto_pk>/crear/', views.crear_tarea, name='crear_tarea'),
    path('<int:pk>/editar/', views.editar_tarea, name='editar_tarea'),
    path('<int:pk>/eliminar/', views.eliminar_tarea, name='eliminar_tarea'),
    path('<int:pk>/estado/', views.cambiar_estado, name='cambiar_estado_tarea'),
]
