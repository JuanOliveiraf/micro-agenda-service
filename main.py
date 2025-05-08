from fastapi import FastAPI, HTTPException
from typing import List
from datetime import date, datetime, timedelta

@app.get("/mentors/{mentor_id}/availability", response_model=List[datetime])
def mentor_availability(mentor_id: int):
    """
    Retorna todos os horários já agendados do mentor na semana atual
    (segunda a domingo).
    """
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=7)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SCHEDULED_DATE
          FROM Mentoring
         WHERE MENTOR_ID = %s
           AND SCHEDULED_DATE BETWEEN %s AND %s
    """, (mentor_id, week_start, week_end))
    occupied = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return occupied

@app.get("/mentorados/{mentorado_id}/availability", response_model=List[datetime])
def mentorado_availability(mentorado_id: int):
    """
    Retorna todos os horários já agendados do mentorado na semana atual.
    """
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=7)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SCHEDULED_DATE
          FROM Mentoring
         WHERE MENTORED_ID = %s
           AND SCHEDULED_DATE BETWEEN %s AND %s
    """, (mentorado_id, week_start, week_end))
    occupied = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return occupied

@app.post("/mentorias", response_model=ScheduleRequest)
def create_mentoria(req: ScheduleRequest):
    """
    Insere um novo agendamento depois de validar disponibilidade
    (sem conflito exato de data/hora para mentor ou mentorado).
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1) Verifica conflito exato de horário para o mentor
        cursor.execute("""
            SELECT COUNT(*) 
              FROM Mentoring 
             WHERE MENTOR_ID = %s 
               AND SCHEDULED_DATE = %s
        """, (req.mentor_id, req.scheduled_datetime))
        if cursor.fetchone()[0] > 0:
            raise HTTPException(400, "Mentor indisponível neste horário")

        # 2) Verifica conflito exato de horário para o mentorado
        cursor.execute("""
            SELECT COUNT(*) 
              FROM Mentoring 
             WHERE MENTORED_ID = %s 
               AND SCHEDULED_DATE = %s
        """, (req.mentorado_id, req.scheduled_datetime))
        if cursor.fetchone()[0] > 0:
            raise HTTPException(400, "Mentorado indisponível neste horário")

        # 3) Insere a mentoria
        cursor.execute("""
            INSERT INTO Mentoring 
                (MENTOR_ID, MENTORED_ID, TOPIC_ID,STATUS,SCHEDULED_DATE,CREATED_DATE,LAST_UPDATE)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            req.mentor_id,
            req.mentorado_id,
            req.topic,
            '',
            req.scheduled_datetime,
            '',
            '',
        ))
        conn.commit()

    finally:
        cursor.close()
        conn.close()

    return req
