# tests/conftest.py
import sys
from pathlib import Path
import io
import pytest

# 1) Que pytest vea tu proyecto
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, StaticPool
from sqlalchemy.orm import sessionmaker

# 2) Importa app y dependencias
from main import app
from database import Base, get_db

# 3) Importa modelos para que Base conozca las tablas
from models.usuario import Usuario      # noqa: F401
from models.categorias import Categoria # noqa: F401
from models.productos import Producto   # noqa: F401

# 4) Motor SQLite para tests
TEST_DB_URL = "sqlite+pysqlite:///:memory:"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False},poolclass=StaticPool,)

# Activa FK en SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5) BD limpia por test (aislamiento)
@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    # DEBUG: imprimir tablas creadas
    print("TABLAS EN LA BD DE PRUEBA:", list(Base.metadata.tables.keys()))
    yield
    Base.metadata.drop_all(bind=engine)

# 6) Override de la dependencia DB
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 7) Cliente HTTP
@pytest.fixture()
def client():
    return TestClient(app)

# 8) Imagen falsa para multipart
@pytest.fixture()
def fake_image_png():
    return ("test.png", io.BytesIO(b"\x89PNG\r\n\x1a\nfake"), "image/png")

