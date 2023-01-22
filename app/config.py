from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOSTNAME: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
