from typing import Optional
from sqlmodel import SQLModel, Field

class Libro(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    autor: str
    paginas: int
    precio: float
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")
