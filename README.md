## Tecnologías
- Frontend: Vue 3 + Vite + Bootstrap 5
- Backend: FastAPI (Python) + SQLAlchemy + JWT
- DB: MySQL

## Requisitos previos
- Node 18+ y npm
- Python 3.10+
- MySQL 8 (o Docker)

---
##.env  edítalo con tus credenciales MySQL:
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_HOST=127.0.0.1
MYSQL_DB=prueba
MYSQL_PORT=3306
DRIVER=pymysql
JWT_SECRET=xxd
JWT_ALGO=HS256
JWT_EXPIRE_MIN=360
---

## Backend
```bash
cd backend
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate


Requisitos mínimos
fastapi
uvicorn[standard]
sqlalchemy
pymysql
python-multipart
pydantic
python-jose[cryptography]
passlib[bcrypt]



