from fastapi import FastAPI
from sqlmodel import select
from app.db import create_all_tables, SessionDep
from app.routes.usuarios import users
from app.routes.libros import books

app = FastAPI(
    title="API FastAPI en AWS EC2 y Amazon RDS",
    description="API RESTful con operaciones CRUD para Usuarios y Libros conectada a PostgreSQL en Amazon RDS",
    version="1.0.0",
    lifespan=create_all_tables,
)

@app.get("/", tags=["health"])
def read_root():
    return {
        "message": "API ejecutándose correctamente en AWS EC2",
        "status": "online"
    }

@app.get("/check-db", tags=["health"])
def check_db(session: SessionDep):
    result = session.exec(select(1)).first()
    return {
        "db_status": "connected",
        "result": result
    }

app.include_router(users)
app.include_router(books)
