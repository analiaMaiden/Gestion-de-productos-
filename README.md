# Gestión de Productos (Vue + FastAPI + MySQL)

Aplicación full-stack para listar, registrar, editar y eliminar **productos** con **Nombre, Descripción, Precio, Imagen y Categoría**.

## Tecnologías
- Frontend: Vue 3 + Vite + Bootstrap 5
- Backend: FastAPI (Python) + SQLAlchemy + JWT
- DB: MySQL
## Requisitos previos
- Node 18+ y npm
- Python 3.10+
- MySQL 8 (o Docker)

---

## Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # editar DATABASE_URL / JWT_SECRET
uvicorn main:app --reload

Requisitos mínimos
fastapi
uvicorn[standard]
sqlalchemy
pymysql
python-multipart
pydantic
python-jose[cryptography]
passlib[bcrypt]
