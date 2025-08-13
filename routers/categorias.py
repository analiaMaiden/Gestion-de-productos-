from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.categorias import Categoria
from routers.auth import get_current_user
from schemas.schema_categoria import CategoriaCreate, CategoriaOut

router = APIRouter(prefix="/categorias", tags=["Categorias"],dependencies=[Depends(get_current_user)])

@router.get("", response_model=list[CategoriaOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Categoria).all()

@router.post("", response_model=CategoriaOut, status_code=201)
def crear(data: CategoriaCreate, db: Session = Depends(get_db)):
    if db.query(Categoria).filter(Categoria.nombre == data.nombre).first():
        raise HTTPException(400, "La categoría ya existe")
    obj = Categoria(nombre=data.nombre)
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.delete("/{categoria_id}", status_code=204)
def borrar(categoria_id: int, db: Session = Depends(get_db)):
    obj = db.get(Categoria, categoria_id)
    if not obj: raise HTTPException(404, "No encontrada")
    db.delete(obj); db.commit()
@router.put("/{categoria_id}", response_model=CategoriaOut)
def actualizar(categoria_id: str, data: CategoriaCreate, db: Session = Depends(get_db)):
    obj = db.get(Categoria, categoria_id)  # funciona con UUID (str) o int
    if not obj:
        raise HTTPException(404, "No encontrada")
    # actualiza campos
    obj.nombre = data.nombre
    obj.descripcion = getattr(data, "descripcion", None)
    db.commit()
    db.refresh(obj)
    return obj