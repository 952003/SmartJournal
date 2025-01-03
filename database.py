from sqlmodel import SQLModel, create_engine
from models import JournalEntry

DATABASE_URL = "sqlite:///journal.db"

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)