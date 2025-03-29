from django.db import models


class Parametro(models.Model):
    codigo_acesso = models.CharField(max_length=255)
    numero_celular = models.CharField(max_length=50)

    class Meta:
        db_table = 'parametros'
