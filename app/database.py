import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Na nuvem, a variavel de ambiente DATABASE_URL aponta para o PostgreSQL.
# No computador, quando ela nao existe, usamos o arquivo devshowcase.db (SQLite).
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./devshowcase.db")

# Alguns provedores entregam a URL comecando com "postgres://",
# mas o SQLAlchemy espera "postgresql://".
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if DATABASE_URL.startswith("sqlite"):
    # check_same_thread=False é necessário para usar SQLite com o FastAPI.
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # pool_pre_ping reconecta sozinho se o banco da nuvem tiver dormido.
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db():
    """Abre uma conexão com o banco para cada requisição e fecha no final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
