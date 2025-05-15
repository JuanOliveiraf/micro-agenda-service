from fastapi import FastAPI,Query
from typing import List
from agendamento import gerar_horarios_disponiveis_em_comum,gerar_agendamento
from models import HorarioDisponivel, Schedule
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ou use ["*"] durante o desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/disponibilidade", response_model=List[HorarioDisponivel])
def buscar_disponibilidade_em_comum(mentor_id: int = Query(...), mentored_id: int = Query(...)):
    return gerar_horarios_disponiveis_em_comum(mentor_id, mentored_id)

@app.post("/schedule")
def receber_agendamento(dados: Schedule):
    return gerar_agendamento(dados)