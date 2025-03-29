from django.shortcuts import redirect, render

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form.errors)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']

            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=senha)

                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Senha incorreta.')
            except User.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')
            context = {'form': form}
            return render(request, 'login/login.html', context=context)
        else:
            messages.error(request, form.errors.as_text())
            print(form.errors.as_text())
            context = {'form': form}
            return render(request, 'login/login.html', context=context)

    else:
        form = LoginForm()
        context = {'form': form}
        return render(request, 'login/login.html', context=context)
    
