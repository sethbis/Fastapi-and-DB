from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import SQLModel, Session, create_engine
from app.config import DATABASE_URL

# Importar modelos para que SQLModel los registre en metadata
from app.models import Usuario, Libro  # noqa: F401

engine = create_engine(DATABASE_URL, echo=True)

def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
