import os
import openai

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database import engine, init_db
from models import JournalEntry
from sqlmodel import Session, select
from datetime import datetime

app = FastAPI



@app.on_event("startup")
def on_startup():
    init_db()

class TextRequest(BaseModel):
    text: str

@app.post("/analyze")
async def analyze_text(request: TextRequest):
    try: 
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": request.text}
            ]
        )
        answer = response["choices"][0]["message"]["content"]
        return {"response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# CRUD SERVICES

@app.post("/entries", response_model=JournalEntry)
async def create_entry(title: str, content: str):
    new_entry = JournalEntry(
        title=title,
        content=content,
        timestamp=datetime.utcnow()
    )
    with Session(engine) as session:
        session.add(new_entry)
        session.commit()
        session.refresh(new_entry)
        return
    
@app.get("/entries", response_model=list[JournalEntry])
async def get_all_entries():
    with Session(engine) as session:
        statement = select(JournalEntry)
        result = session.exec(statement).all()
        return result
    
@app.get("/entries/{entry_id}", response_model=JournalEntry)
async def get_entry(entry_id: int):
    with Session(engine) as session:
        entry = session.get(JournalEntry, entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        return entry
    
@app.put("/entries/{entry_id}", response_model=JournalEntry)
async def update_entry(entry_id: int, title: str = None, content: str = None):
    with Session(engine) as session:
        entry = session.get(JournalEntry, entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        if title:
            entry.title = title
        if content:
            entry.content = content
        session.add(entry)
        session.commit()
        session.refresh(entry)
        return entry
    
@app.delete("/entries/{entry_id}")
async def delete_entry(entry_id: int):
    with Session(engine) as session:
        entry = session.get(JournalEntry, entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        session.delete(entry)
        session.commit()
        return {"ok": True, "deleted_id": entry_id}
    
@app.get("/")
async def root():
    return {"message": "SmartJournal API is running with DB!"}
