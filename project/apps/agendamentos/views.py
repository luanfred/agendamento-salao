from django.shortcuts import render, redirect
from servicos.models import Servico
from .models import Agendamento, status_agendamento
from django.http import JsonResponse
from django.contrib import messages as message
from datetime import datetime, timedelta
from django.http import JsonResponse
from .models import Servico, Agendamento
from django.contrib.auth.decorators import login_required
from parametros.models import Parametro

def registar_agendamento(request):
    if request.method == "POST":
        cliente = request.user
        servico_id = request.POST.get("servico")
        servico = Servico.objects.get(id=servico_id)
        data_escolhida = request.POST.get("data")
        horario = request.POST.get("horario")
        status = status_agendamento[0][1]
        
        agendamento = Agendamento(
            cliente=cliente,
            servico_id=servico.id,
            data=data_escolhida,
            horario=horario,
            status=status,
        )
        agendamento.save()
        message.success(request, "Agendamento realizado com sucesso!")
        return redirect("registar_agendamento")

    else:
        servicos = Servico.objects.all()
        context = {
            "servicos": servicos,
        }
        return render(request, "agendamentos/registrar.html", context=context)


def horarios_disponiveis(request):
    servico_id = request.GET.get("servico")
    data_escolhida = request.GET.get("data")  # Formato: YYYY-MM-DD
    
    if not servico_id or not data_escolhida:
        return JsonResponse({"erro": "Serviço ou data não selecionados"}, status=400)

    # Criar lista de horários base (de hora em hora)
    horarios_base = [datetime.strptime(f"{h:02d}:00", "%H:%M").time() for h in range(8, 19)]  # 08:00 até 18:00

    # Buscar horários ocupados no banco
    horarios_ocupados = list(Agendamento.objects.filter(data=data_escolhida).values_list("horario", flat=True))

    # Filtrar horários disponíveis, garantindo que nenhum intervalo esteja sobreposto
    horarios_livres = []
    for horario in horarios_base:
        if all(
            not (h <= horario < (datetime.combine(datetime.today(), h) + timedelta(hours=1)).time())
            for h in horarios_ocupados
        ):
            horarios_livres.append(horario.strftime("%H:%M"))

    return JsonResponse({"horarios": horarios_livres, "data": data_escolhida, "servico_id": servico_id}, status=200)


def listar_agendamentos(request):
    agendamentos = Agendamento.objects.filter(cliente=request.user).order_by("-data", "-horario")
    context = {
        "agendamentos": agendamentos,
    }
    return render(request, "agendamentos/listar_agendamentos.html", context=context)

def alterar_horario(request, id):
    if request.method == "POST":
        agendamento = Agendamento.objects.filter(id=id).first()
        if not agendamento:
            message.error(request, "Agendamento não encontrado.")
            return redirect("listar_agendamentos")

        data_escolhida = request.POST.get("data")
        horario = request.POST.get("horario")
        data_hoje = datetime.today().date()
    
        if data_escolhida < (data_hoje + timedelta(days=2)).strftime("%Y-%m-%d"):
            parametro = Parametro.objects.first()
            if parametro and parametro.numero_celular:
                numero_celular = parametro.numero_celular
                message.error(request, f"Alteração só permitida com 2 dias de antecedência. Ligue para {numero_celular} para mais informações.")
            else:
                message.error(request, "Alteração só permitida com 2 dias de antecedência.")

            return redirect("listar_agendamentos")

        agendamento.data = data_escolhida
        agendamento.horario = horario
        agendamento.save()
        
        
        message.success(request, "Horário alterado com sucesso!")
        return redirect("listar_agendamentos")
    else:
        agendamento = Agendamento.objects.filter(id=id).first()
        context = {
            "agendamento": agendamento,
        }
        return render(request, "agendamentos/alterar_horario.html", context=context)


def listar_todos_agendamentos(request):
    status_filter = request.GET.get('status')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    # Buscar todos os agendamentos inicialmente
    agendamentos = Agendamento.objects.all()

    # Filtrar por status se o usuário selecionar um
    if status_filter:
        agendamentos = agendamentos.filter(status=status_filter)

    # Aplicar filtro de intervalo de datas
    if data_inicio and data_fim:
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d").date()
        agendamentos = agendamentos.filter(data__range=[data_inicio, data_fim])
    elif data_inicio:  # Caso o usuário preencha apenas a data de início
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
        agendamentos = agendamentos.filter(data__gte=data_inicio)
    elif data_fim:  # Caso o usuário preencha apenas a data de fim
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d").date()
        agendamentos = agendamentos.filter(data__lte=data_fim)

    context = {
        'agendamentos': agendamentos,
        'status_agendamento': dict(status_agendamento),  # Para popular o select de status
    }
    return render(request, "agendamentos/listar_todos_agendamentos.html", context=context)


def editar_agendamento(request, id):
    agendamento = Agendamento.objects.filter(id=id).first()
    if not agendamento:
        message.error(request, "Agendamento não encontrado.")
        return redirect("listar_todos_agendamentos")

    if request.method == "POST":
        novo_status = request.POST.get("status")
        novo_horario = request.POST.get("horario")
        nova_data = request.POST.get("data")
        
        try:
            # Tentando converter a string de horário para um objeto do tipo time
            novo_horario_obj = datetime.strptime(novo_horario, "%H:%M").time()
            nova_data_obj = datetime.strptime(nova_data, "%Y-%m-%d").date()
            agendamento.horario = novo_horario_obj
            agendamento.data = nova_data_obj

            if Agendamento.objects.filter(horario=novo_horario, data=nova_data).exclude(id=id).exists():
                dict_status = {}
                for status in status_agendamento:
                    dict_status[status[0]] = status[1]
                context = {
                    "agendamento": agendamento,
                    "status_agendamento": dict_status,
                }
                message.error(request, "Horário já agendado.")
                return render(request, "agendamentos/editar.html",context)
            
        except ValueError:
            message.error(request, "Formato de horário inválido. Use HH:MM.")
            return render(request, "agendamentos/editar.html", {"agendamento": agendamento})
        
        for status in status_agendamento:
            if novo_status == status[0]:
                agendamento.status = status[1]
                break


        agendamento.save()
        return redirect("listar_todos_agendamentos")
    else:
        dict_status = {}
        for status in status_agendamento:
            dict_status[status[0]] = status[1]
        context = {
            "agendamento": agendamento,
            "status_agendamento": dict_status,
        }
        return render(request, "agendamentos/editar.html", context=context)
    

def detalhes_agendamento(request, id):
    agendamento = Agendamento.objects.filter(id=id).first()
    if not agendamento:
        message.error(request, "Agendamento não encontrado.")
        return redirect("listar_todos_agendamentos")

    context = {
        "agendamento": agendamento,
    }
    return render(request, "agendamentos/detalhes.html", context=context)
    
