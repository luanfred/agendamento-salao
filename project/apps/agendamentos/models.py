from django.db import models
from django.contrib.auth.models import User
from servicos.models import Servico 

status_agendamento = [
    ("pendente", "Pendente"), 
    ("confirmado", "Confirmado"),
    ("cancelado", "Cancelado"),
    ("finalizado", "Finalizado"),
]

class Agendamento(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)  
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    data = models.DateField() 
    horario = models.TimeField()
    status = models.CharField(
        max_length=20, 
        choices=status_agendamento
    )

    class Meta:
        unique_together = ('data', 'horario')  # Garante que não há dois agendamentos no mesmo horário