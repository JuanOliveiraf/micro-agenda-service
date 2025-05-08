from pydantic import BaseModel

class Mentor(BaseModel):
    ID: int

class ScheduleRequest(BaseModel):
    MENTOR_ID: int
    MENTORED_ID: int
    TOPIC_ID: str
    SCHEDULED_DATE: datetime
    
class CancelRequest(BaseModel):
    MENTOR_ID: int
    MENTORED_ID: int
    SCHEDULED_DATE: datetime