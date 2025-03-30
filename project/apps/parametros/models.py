from django.db import models


class Parametro(models.Model):
    codigo_acesso = models.CharField(max_length=255)
    numero_celular = models.CharField(max_length=50)

    class Meta:
        db_table = 'parametros'

    def verificar_chave_acesso(self, chave: str):
        """
        Verifica se a chave de acesso é válida.
        :param chave: Chave de acesso a ser verificada.
        :return: True se a chave for válida, False caso contrário.
        """
        return self.codigo_acesso == chave
