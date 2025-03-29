from django.db import models

class Servico(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    duracao = models.DurationField()
    preco = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'servicos'


    def duracao_formatada(self):
        total_segundos = int(self.duracao.total_seconds())
        horas = total_segundos // 3600
        minutos = (total_segundos % 3600) // 60
        return f"{horas:02d}:{minutos:02d}"