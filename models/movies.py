# user.py (modelo)
from pydantic import BaseModel
from datetime import datetime

class movieBase(BaseModel):
    title: str
    uri: str
    poster: str
    producer: str
    subtitle: str
    description: str
    owner: str
    likes: int
    messages: int

class movieDB(movieBase):
    created_at: datetime = datetime.utcnow()
