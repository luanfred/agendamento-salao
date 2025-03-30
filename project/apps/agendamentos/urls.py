from django.urls import path
from . import views

urlpatterns = [
    path("registrar/", views.registar_agendamento, name="registar_agendamento"),
    path("horarios-disponiveis/", views.horarios_disponiveis, name="horarios_disponiveis"),
]