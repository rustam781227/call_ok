from os import getenv

from dotenv import load_dotenv
from pydantic import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    USER: str = getenv('POSTGRES_USER', 'postgres')
    PASSWORD: str = getenv('POSTGRES_PASSWORD', 'postgres')
    HOST: str = getenv('DB_HOST', '127.0.0.1')
    PORT: str = getenv('DB_PORT', '5432')
    DB_NAME: str = getenv('DB_NAME', 'music_storage')


settings = Settings()
