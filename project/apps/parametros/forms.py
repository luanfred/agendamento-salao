
from typing import Any
from django import forms
from .models import Parametro


class ParametroForm(forms.ModelForm):
    class Meta:
        model = Parametro
        fields = ['codigo_acesso', 'numero_celular']
        widgets = {
            'codigo_acesso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código de Acesso'}),
            'numero_celular': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de Celular ex: (14) 99888-8888'}),
        }
        labels = {
            'codigo_acesso': 'Código de Acesso',
            'numero_celular': 'Número de Celular do Responsável',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        chave_nova = cleaned_data.get('codigo_acesso')
        numero_salao_novo = cleaned_data.get('numero_celular')

        # Se for um novo registro, não precisa validar
        if not self.instance.pk:
            return cleaned_data

        # Buscar os valores antigos do banco
        parametro_antigo = Parametro.objects.filter(pk=self.instance.pk).first()

        if parametro_antigo:
            chave_antiga = parametro_antigo.codigo_acesso
            numero_salao_antigo = parametro_antigo.numero_celular

            # Permitir salvar caso qualquer um dos campos tenha mudado
            if chave_nova != chave_antiga or numero_salao_novo != numero_salao_antigo:
                return cleaned_data

        raise forms.ValidationError("Nenhuma alteração foi feita nos dados.")
    