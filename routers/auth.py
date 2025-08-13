# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models.usuario import Usuario
from schemas.schema_usuario import LoginIn, UserOut
from security import hash_password, verify_password, create_access_token, decode_token

router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/register", response_model=UserOut, status_code=201)
def register(data: LoginIn, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.username == data.username).first():
        raise HTTPException(400, "Usuario ya existe")
    u = Usuario(username=data.username, password_hash=hash_password(data.password))
    db.add(u); db.commit(); db.refresh(u)
    return {"id": u.id, "username": u.username}
@router.post("/login")
def login(data: LoginIn, db: Session = Depends(get_db)):
    u = db.query(Usuario).filter(Usuario.username == data.username).first()
    if not u or not verify_password(data.password, u.password_hash):
        raise HTTPException(401, "Credenciales inválidas")
    token = create_access_token(u.id)
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(401, "Token inválido o expirado")
    uid = (payload["sub"])
    user = db.get(Usuario, uid)
    if not user:
        raise HTTPException(401, "Usuario no encontrado")
    return user

@router.get("/me", response_model=UserOut)
def me(current: Usuario = Depends(get_current_user)):
    return current
