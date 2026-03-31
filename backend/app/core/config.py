from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+aiomysql://tableorder:tableorder@db:3306/tableorder"
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 16
    UPLOAD_DIR: str = "app/uploads"

    class Config:
        env_file = ".env"


settings = Settings()
