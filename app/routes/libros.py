from typing import List
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.models.libro import Libro
from app.db import SessionDep

books = APIRouter(prefix="/libros", tags=["libros"])

@books.post("/", response_model=Libro)
def crear_libro(libro: Libro, session: SessionDep):
    session.add(libro)
    session.commit()
    session.refresh(libro)
    return libro

@books.get("/", response_model=List[Libro])
def listar_libros(session: SessionDep):
    return session.exec(select(Libro)).all()

@books.get("/{libro_id}", response_model=Libro)
def obtener_libro(libro_id: int, session: SessionDep):
    libro = session.get(Libro, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@books.put("/{libro_id}", response_model=Libro)
def actualizar_libro(libro_id: int, datos: Libro, session: SessionDep):
    libro = session.get(Libro, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    libro.titulo = datos.titulo
    libro.autor = datos.autor
    libro.paginas = datos.paginas
    libro.precio = datos.precio
    libro.usuario_id = datos.usuario_id
    session.add(libro)
    session.commit()
    session.refresh(libro)
    return libro

@books.delete("/{libro_id}")
def eliminar_libro(libro_id: int, session: SessionDep):
    libro = session.get(Libro, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    session.delete(libro)
    session.commit()
    return {"ok": True}
