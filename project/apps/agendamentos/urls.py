from django.urls import path
from . import views

urlpatterns = [
    path("registrar/", views.registar_agendamento, name="registar_agendamento"),
    path("horarios-disponiveis/", views.horarios_disponiveis, name="horarios_disponiveis"),
    path("cliente/listar/", views.listar_agendamentos, name="listar_agendamentos"),
    path("alterar-horario/<int:id>/", views.alterar_horario, name="alterar_horario"),
    path("listar/", views.listar_todos_agendamentos, name="listar_todos_agendamentos"),
    path("editar/<int:id>/", views.editar_agendamento, name="editar_agendamento"),
    path("detalhes/<int:id>/", views.detalhes_agendamento, name="detalhes_agendamento"),

]