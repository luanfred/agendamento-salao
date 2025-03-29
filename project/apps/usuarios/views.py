from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .forms import CriarUsuarioForm

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CriarUsuarioForm

def usuario_registrar(request):
    if request.method == 'POST':
        form = CriarUsuarioForm(request.POST)
        if form.is_valid():
            primeiro_nome = form.cleaned_data['primeiro_nome']
            ultimo_nome = form.cleaned_data['ultimo_nome']
            senha = form.cleaned_data['senha']
            email = form.cleaned_data['email']

            # Verifica se o usuário já existe
            if User.objects.filter(username=email).exists():
                messages.error(request, 'Usuário já existe.')
                return redirect('usuarios_registrar')

            user = User(
                username=email,
                first_name=primeiro_nome,
                last_name=ultimo_nome,
                email=email,
            )
            user.set_password(senha)
            user.save()

            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('login')
        else:
            # Se o formulário não for válido, exibe as mensagens de erro
            for error in form.errors.values():
                messages.error(request, str(error))

            return render(request, 'usuarios/registrar.html', {'form': form})

    else:
        form = CriarUsuarioForm()

        context = {'form': form}
        return render(request, 'usuarios/registrar.html', context)

