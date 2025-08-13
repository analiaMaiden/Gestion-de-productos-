from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import get_db
from models.productos import Producto
from models.categorias import Categoria
from routers.auth import get_current_user

router = APIRouter(prefix="/productos", tags=["productos"], dependencies=[Depends(get_current_user)])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.get("")
def listar(db: Session = Depends(get_db)):
    return db.query(Producto).all()

@router.post("", status_code=201)
async def crear(
    nombre: str = Form(...),
    descripcion: str = Form(""),
    precio: float = Form(...),
    categoria_id: str = Form(...),
    imagen: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    if not db.get(Categoria, categoria_id):
        raise HTTPException(400, "Categoría inexistente")

    ruta = None
    if imagen and imagen.filename:
        ext = Path(imagen.filename).suffix or ""
        filename = f"{uuid4().hex}{ext}"
        ruta_path = UPLOAD_DIR / filename
        with ruta_path.open("wb") as f:
            f.write(await imagen.read())
        ruta = str(ruta_path)

    p = Producto(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        imagen=ruta,
        categoria_id=categoria_id
    )
    db.add(p); db.commit(); db.refresh(p)
    return p

@router.put("/{producto_id}")
async def actualizar(
    producto_id: str,
    nombre: str = Form(...),
    descripcion: str = Form(""),
    precio: float = Form(...),
    categoria_id: str = Form(...),
    imagen: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    p = db.get(Producto, producto_id)
    if not p:
        raise HTTPException(404, "No encontrado")
    if not db.get(Categoria, categoria_id):
        raise HTTPException(400, "Categoría inexistente")

    p.nombre = nombre
    p.descripcion = descripcion
    p.precio = precio
    p.categoria_id = categoria_id

    # Solo guardar si realmente subieron un archivo con nombre
    if imagen and imagen.filename:
        ext = Path(imagen.filename).suffix or ""
        filename = f"{uuid4().hex}{ext}"
        ruta_path = UPLOAD_DIR / filename
        with ruta_path.open("wb") as f:
            f.write(await imagen.read())
        p.imagen = str(ruta_path)

    db.commit(); db.refresh(p)
    return p

@router.delete("/{producto_id}", status_code=204)
def borrar(producto_id: str, db: Session = Depends(get_db)):
    p = db.get(Producto, producto_id)
    if not p:
        raise HTTPException(404, "No encontrado")
    db.delete(p); db.commit()
    return None
