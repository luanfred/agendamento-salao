from django.shortcuts import redirect, render
from .forms import ParametroForm
from django.contrib import messages
from .models import Parametro
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    parametro = Parametro.objects.first()  # Obtém o primeiro registro de Parametro

    if request.method == "POST":
        form = ParametroForm(request.POST, instance=parametro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Parâmetro salvo com sucesso!')
            return redirect('index_parametro') 
        else:
            messages.error(request, 'Nenhum dado foi alterado')
    else:
        form = ParametroForm(instance=parametro)

    return render(request, 'parametros/index.html', {'form': form})
    
