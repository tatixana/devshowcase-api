from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# O arquivo devshowcase.db é criado na pasta onde a API é iniciada.
DATABASE_URL = "sqlite:///./devshowcase.db"

# check_same_thread=False é necessário para usar SQLite com o FastAPI.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

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
