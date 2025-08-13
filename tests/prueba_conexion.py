from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DB = os.getenv("MYSQL_DB")

# Crear cadena de conexión
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# Crear motor de conexión
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT DATABASE();"))
        db_name = result.scalar()
        print(f"✅ Conexión exitosa a la base de datos: {db_name}")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
