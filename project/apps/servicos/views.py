from django.shortcuts import redirect, render
from .models import Servico
from .forms import ServicoForm

def index(request):
    if request.method == 'GET':
        servicos = Servico.objects.all()
        return render(request, 'servicos/index.html', {'servicos': servicos})
    else:
        return redirect('index_servico')


def registrar_servico(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index_servico')
        else:
            context = {
                'form': form,
                'acao': 'Adicionar',
            }
            return render(request, 'servicos/registrar.html', context=context)
    else:
        form = ServicoForm()
        context = {
            'form': form,
            'acao': 'Adicionar',
        }
        return render(request, 'servicos/registrar.html', context=context)


def editar_servico(request, id):
    servico = Servico.objects.get(id=id)
    if request.method == 'POST':
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            return redirect('index_servico')
        else:
            context = {
                'form': form,
                'acao': 'Editar',
            }
            return render(request, 'servicos/registrar.html', context=context)
    else:
        form = ServicoForm(instance=servico)
        print(form.instance.duracao)
        context = {
            'form': form,
            'acao': 'Editar',
        }
        return render(request, 'servicos/registrar.html', context=context)
    

def deletar_servico(request, id):
    servico = Servico.objects.get(id=id)
    if request.method == 'POST':
        servico.delete()
        return redirect('index_servico')
    else:
        context = {
            'servico': servico,
        }
        return render(request, 'servicos/confirmar_deletar_servico.html', context=context)
    

def detalhes_servico(request, id):
    servico = Servico.objects.get(id=id)
    form = ServicoForm(instance=servico)
    context = {
        'form': form,
        'acao': 'Detalhes',
    }
    return render(request, 'servicos/detalhes.html', context=context)