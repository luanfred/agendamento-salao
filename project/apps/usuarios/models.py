from django.db import models
from django.contrib.auth.models import User
class Usuario(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario', db_column='user_id', null=True)
    telefone = models.CharField(max_length=15, unique=True)
    funcionario = models.BooleanField(default=False)
    class Meta:
        db_table = 'usuarios'
        