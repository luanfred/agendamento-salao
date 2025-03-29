from django import forms
from django.core.exceptions import ValidationError
import re

class CriarUsuarioForm(forms.Form):
    primeiro_nome = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Primeiro Nome',
        })
    )
    ultimo_nome = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Último Nome',
        })
    )
    telefone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Telefone',
        })
    )
    email = forms.EmailField(
        max_length=50,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
        })
    )
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Senha',
        })
    )
    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar Senha',
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmar_senha = cleaned_data.get("confirmar_senha")

        if senha != confirmar_senha:
            raise ValidationError("As senhas não coincidem.")

        # Validação de força da senha (mínimo de 8 caracteres, pelo menos uma letra maiúscula e um número)
        if senha:
            if len(senha) < 8:
                raise ValidationError("A senha deve ter pelo menos 8 caracteres.")
            if not re.search(r'[A-Z]', senha):
                raise ValidationError("A senha deve conter pelo menos uma letra maiúscula.")
            if not re.search(r'[0-9]', senha):
                raise ValidationError("A senha deve conter pelo menos um número.")

        return cleaned_data
    
    
