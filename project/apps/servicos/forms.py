from datetime import timedelta
from django import forms
from .models import Servico

class ServicoForm(forms.ModelForm):
    
    def clean(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get('nome')
        duracao = cleaned_data.get('duracao')
        preco = cleaned_data.get('preco')

        if not nome or not duracao or not preco:
            raise forms.ValidationError("Todos os campos são obrigatórios.")
        
        return cleaned_data

    def clean_duracao(self):
        duracao_str = str(self.cleaned_data.get('duracao'))
        if duracao_str:
            try:
                horas = float(duracao_str.split(':')[1])
                minutos = float(duracao_str.split(':')[2])
                return timedelta(hours=horas, minutes=minutos)
            except:
                raise forms.ValidationError("Formato de duração inválido. Use HH:MM.")
        else:
            raise forms.ValidationError("A duração é obrigatória.")
    
    def clean_preco(self):
        preco_str = str(self.cleaned_data.get('preco'))
        if preco_str:
            try:
                preco = float(preco_str.replace(',', '.'))
                if preco < 0:
                    raise forms.ValidationError("O preço não pode ser negativo.")
                return preco
            except ValueError:
                raise forms.ValidationError("Formato de preço inválido. Use R$ 0,00.")
        else:
            raise forms.ValidationError("O preço é obrigatório.")
        

    class Meta:
        model = Servico
        fields = ['nome', 'descricao', 'duracao', 'preco']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Serviço'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'duracao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 01:30 (1 hora e meia)',
                'pattern': r'^\d{1,2}:\d{2}$',  # opcional para validação HTML5
            }),
            'preco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'R$ 0,00'}),
        }
        error_messages = {
            'nome': {
                'required': 'O nome do serviço é obrigatório.',
                'max_length': 'O nome do serviço deve ter no máximo 100 caracteres.'
            },
            'descricao': {
                'required': 'A descrição do serviço é obrigatória.',
                'max_length': 'A descrição do serviço deve ter no máximo 500 caracteres.'
            },
            'duracao': {
                'required': 'A duração do serviço é obrigatória.',
            },
            'preco': {
                'required': 'O preço do serviço é obrigatório.',
                'invalid': 'O preço deve ser um número válido.',
            }
        }
        labels = {
            'nome': 'Nome',
            'descricao': 'Descrição',
            'duracao': 'Duração',
            'preco': 'Preço',
        }
