from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConnectionSettings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASS: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_LIFETIME: int
    REFRESH_TOKEN_LIFETIME: int
    EMAIL_TOKEN_LIFETIME: int
    PASSWORD_RESET_TOKEN_LIFETIME: int

    @computed_field(return_type=str)
    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASS}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_NAME}"

    model_config = SettingsConfigDict(env_file=".env")

