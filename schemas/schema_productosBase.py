from pydantic import BaseModel, Field
from typing import Optional

class ProductoBase(BaseModel):
    nombre: str = Field(..., max_length=150)
    descripcion: Optional[str] = None
    precio: float
    categoria_id: int

class ProductoCreate(ProductoBase):
    imagen: Optional[str] = None

class ProductoUpdate(ProductoBase):
    imagen: Optional[str] = None

class ProductoOut(ProductoBase):
    id: int
    imagen: Optional[str] = None
    class Config: from_attributes = True
