from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Parametro

@receiver(post_migrate)
def criar_registro_padrao(sender, **kwargs):
    if sender.name == 'parametros':  
        if not Parametro.objects.exists(): 
            Parametro.objects.create(
                codigo_acesso="123456",
                numero_celular="(11) 99999-9999"
            )
            print("Registro padrão de Parametro criado com sucesso!")