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