from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_servico'),
    path('registrar/', views.registrar_servico, name='registrar_servico'),
    path('editar/<int:id>/', views.editar_servico, name='editar_servico'),
    path('deletar/<int:id>/', views.deletar_servico, name='deletar_servico'),
    path('detalhes/<int:id>/', views.detalhes_servico, name='detalhes_servico'),
]
