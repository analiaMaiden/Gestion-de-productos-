from pydantic import BaseModel, Field

class CategoriaBase(BaseModel):
    nombre: str = Field(..., max_length=100)

class CategoriaCreate(CategoriaBase): pass

class CategoriaOut(CategoriaBase):
    id: int
    class Config: from_attributes = True