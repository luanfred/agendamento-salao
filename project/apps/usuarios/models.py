from django.db import models
from django.contrib.auth.models import User
class Usuario(models.Model):
    telefone = models.CharField(max_length=15, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuario', null=False, blank=True, db_column='user_id')
    funcionario = models.BooleanField(default=False)
    class Meta:
        db_table = 'usuarios'
        