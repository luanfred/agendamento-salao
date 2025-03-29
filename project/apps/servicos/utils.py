
from datetime import time, timedelta, datetime

def gerar_horarios_disponiveis(data_escolhida):
    horarios_disponiveis = []
    inicio = time(8, 0)
    fim = time(18, 0)
    intervalo = timedelta(minutes=30)

    atual = datetime.combine(data_escolhida, inicio)
    fim_datetime = datetime.combine(data_escolhida, fim)

    # Pega os agendamentos existentes do dia
    # agendamentos_existentes = Agendamento.objects.filter(data=data_escolhida)
    agendamentos_existentes = []  # Simulação de agendamentos existentes
    horarios_ocupados = [ag.horario for ag in agendamentos_existentes]

    while atual <= fim_datetime:
        horario = atual.time()
        if horario not in horarios_ocupados:
            horarios_disponiveis.append(horario)
        atual += intervalo

    return horarios_disponiveis
