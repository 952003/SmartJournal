from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class JournalEntry(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    timestamp: datetime