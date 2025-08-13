# database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

user = os.getenv("MYSQL_USER")
pwd  = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST", "127.0.0.1")
db   = os.getenv("MYSQL_DB", "prueba")
port = os.getenv("MYSQL_PORT", "3306")
driver = os.getenv("DRIVER", "pymysql")  # o 'mysqlclient'

DATABASE_URL = f"mysql+{driver}://{user}:{pwd}@{host}:{port}/{db}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
