from django.urls import path
from . import views

urlpatterns = [
    path("registrar/", views.registar_agendamento, name="registar_agendamento"),
    path("horarios-disponiveis/", views.horarios_disponiveis, name="horarios_disponiveis"),
    path("listar/", views.listar_agendamentos, name="listar_agendamentos"),
    path("alterar-horario/<int:id>/", views.alterar_horario, name="alterar_horario"),
]