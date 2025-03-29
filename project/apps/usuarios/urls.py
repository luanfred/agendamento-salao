from django.urls import path

from usuarios import views

urlpatterns = [
    path('registrar/', views.usuario_registrar, name='usuarios_registrar'),
]
