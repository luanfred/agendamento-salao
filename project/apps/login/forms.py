from django import forms

class LoginForm(forms.Form):
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
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        senha = cleaned_data.get("senha")

        if not email or not senha:
            raise forms.ValidationError("Email e senha são obrigatórios.")

        return cleaned_data
