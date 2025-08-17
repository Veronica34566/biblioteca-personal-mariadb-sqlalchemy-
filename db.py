from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import os
from dotenv import load_dotenv

load_dotenv()

# Opción A (recomendada por facilidad de instalación): usar PyMySQL
# URL: mysql+pymysql://usuario:password@host:puerto/base

DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "biblioteca")

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# Opción B (dialecto MariaDB nativo):
# Requiere instalar mariadb==1.x
# DB_URL = f"mariadb+mariadbconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DB_URL,
    echo=False,            # pon True si quieres ver el SQL generado
    pool_pre_ping=True,    # detecta conexiones caídas
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    """Dependencia/Contexto de sesión para usar con with."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection():
    try:
        with engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")
        return True
    except OperationalError as e:
        print("[ERROR] No se pudo conectar a la base de datos:", e)
        return False
