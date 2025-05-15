from typing import List, Dict
from db import get_connection
from datetime import datetime, timedelta
from models import Schedule

def gerar_horarios_disponiveis_em_comum(mentor_id: int, mentored_id: int) -> List[Dict]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    agora = datetime.now()
    inicio_mes = agora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if agora.month == 12:
        inicio_prox_mes = agora.replace(year=agora.year + 1, month=1, day=1)
    else:
        inicio_prox_mes = agora.replace(month=agora.month + 1, day=1)

    # Buscar agendamentos do mês atual
    cursor.execute("""
        SELECT scheduled_date
        FROM mentorings
        WHERE (mentor_id = %s OR mentored_id = %s)
        AND scheduled_date >= %s AND scheduled_date < %s
    """, (mentor_id, mentored_id, agora, inicio_prox_mes))  # já filtra a partir de agora

    agendados = {
        row['scheduled_date'].replace(minute=0, second=0, microsecond=0)
        for row in cursor.fetchall()
    }

    horarios_disponiveis = []
    dia = inicio_mes
    while dia < inicio_prox_mes:
        if dia.weekday() < 5:  # segunda a sexta
            for hora in range(9, 18):
                dt = dia.replace(hour=hora, minute=0, second=0, microsecond=0)
                if dt >= agora and dt not in agendados:
                    horarios_disponiveis.append({
                        'data': dt.strftime('%Y-%m-%d'),
                        'hora': dt.strftime('%H:%M')
                    })
        dia += timedelta(days=1)

    cursor.close()
    conn.close()

    return horarios_disponiveis

def gerar_agendamento(dados: Schedule):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""INSERT INTO mentorings 
                   (name,
                   mentor_id,
                   mentored_id,
                   topic_id,
                   concluded,
                   scheduled_date,
                   created_date,
                   last_update,
                   rating) 
                   values (%s,
                    %s, 
                    %s,
                    %s, 
                    false,
                    %s, 
                    DATE_SUB(NOW(),INTERVAL 3 HOUR),
                    DATE_SUB(NOW(),INTERVAL 3 HOUR),
                    null)""", (dados.name,dados.mentor_id,dados.mentored_id,dados.topic_id,dados.scheduled_date))
    
    conn.commit()

    cursor.close()
    conn.close()

    return