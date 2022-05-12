from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from apps.src.config import Config

SQLALCHEMY_DATABASE_URL= Config.database_url('mysql')

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # sqlite를 사용하는 경우에만 connect_args 필요
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

# Dependancy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()