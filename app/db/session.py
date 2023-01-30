from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

SQLALCHEMY_DATABASE_URL = (
    f'postgresql://{settings.POSTGRES_USER}:'
    f'{settings.POSTGRES_PASSWORD}@'
    f'{settings.POSTGRES_HOSTNAME}:'
    f'{settings.DATABASE_PORT}/'
    f'{settings.POSTGRES_DB}'
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
