from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .forms import CriarUsuarioForm

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CriarUsuarioForm
from usuarios.models import Usuario
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from parametros.models import Parametro

@login_required
def home(request):
    return render(request, 'home/home.html')


def usuario_registrar(request):
    if request.method == 'POST':
        form = CriarUsuarioForm(request.POST)
        if form.is_valid():
            primeiro_nome = form.cleaned_data['primeiro_nome']
            ultimo_nome = form.cleaned_data['ultimo_nome']
            senha = form.cleaned_data['senha']
            email = form.cleaned_data['email']
            telefone = form.cleaned_data['telefone']
            is_functionario = request.POST.get('is-funcionario')
            chave_acesso = request.POST.get('chave_acesso', None)

            # Verifica se a chave de acesso é a correta
            if is_functionario == 'S':
                is_functionario = True
                parametro = Parametro.objects.first()
                if parametro and not parametro.verificar_chave_acesso(chave_acesso):
                    messages.error(request, 'Chave de acesso inválida.')
                    return render(request, 'usuarios/registrar.html', {'form': form})
                elif not parametro:
                    messages.error(request, 'Parâmetro de configuração não encontrado.')
                    return render(request, 'usuarios/registrar.html', {'form': form})
            else:
                is_functionario = False


            # Verifica se o usuário já existe
            if User.objects.filter(username=email).exists():
                messages.error(request, 'Usuário já existe.')
                return render(request, 'usuarios/registrar.html', {'form': form})

            user = User(
                username=email,
                first_name=primeiro_nome,
                last_name=ultimo_nome,
                email=email,
            )
            user.set_password(senha)
            user.save()

            usuario = Usuario(
                telefone=telefone,
                user_id=user,
                funcionario=is_functionario
            )
            usuario.save()

            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, str(error))

            return render(request, 'usuarios/registrar.html', {'form': form})

    else:
        form = CriarUsuarioForm()

        context = {'form': form}
        return render(request, 'usuarios/registrar.html', context)


@login_required
def deslogar_usuario(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
    else:
        messages.error(request, 'Usuário não está autenticado.')
    return redirect('login')
