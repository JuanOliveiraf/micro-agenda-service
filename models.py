
from pydantic import BaseModel
from datetime import datetime

class HorarioDisponivel(BaseModel):
    data: str    # ex: "2025-05-15"
    hora: str    # ex: "14:00"

class Schedule(BaseModel):
    mentor_id: int
    mentored_id: int
    name: str
    topic_id: int
    scheduled_date: datetime
