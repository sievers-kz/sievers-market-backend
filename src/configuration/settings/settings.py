from typing import Tuple, Type

from pydantic import Field, computed_field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return init_settings, env_settings, dotenv_settings


class PostgresSettings(BaseConfig):
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT")
    name: str = Field(alias="POSTGRES_NAME")
    user: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASS")

    @computed_field(return_type=str)
    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://{self.user}:"
            f"{self.password}@{self.host}:"
            f"{self.port}/{self.name}"
        )


class AuthenticationSettings(BaseConfig):
    secret_key: str = Field(alias="SECRET_KEY")
    algorithm: str = Field(alias="ALGORITHM")
    access_token_lifetime: int = Field(alias="ACCESS_TOKEN_LIFETIME")
    refresh_token_lifetime: int = Field(alias="REFRESH_TOKEN_LIFETIME")


class MinioConfig(BaseConfig):
    endpoint: str = Field(alias="MINIO_ENDPOINT")
    access_key: str = Field(alias="MINIO_ROOT_USER")
    secret_key: str = Field(alias="MINIO_ROOT_PASSWORD")
    bucket_name: str = Field(alias="MINIO_BUCKET_NAME")
    secure_config: bool = Field(alias="MINIO_SECURE_CONFIG")


class RedisConfig(BaseConfig):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT")
    db: int = Field(alias="REDIS_DB")
    password: str | None = Field(None, alias="REDIS_PASSWORD")


class ResendSettings(BaseConfig):
    api_key: str = Field(alias="RESEND_API_KEY")
    from_email: str = Field(alias="RESEND_FROM_EMAIL")


class SentryConfig(BaseConfig):
    dsn: str | None = Field(None, alias="SENTRY_DSN")
    mode: str = Field(alias="MODE")


class KGDSettings(BaseConfig):
    portal_token: str = Field(alias="KGD_PORTAL_TOKEN")


class MeilisearchConfig(BaseConfig):
    url: str = Field(alias="MEILISEARCH_URL")
    key: str = Field(alias="MEILISEARCH_KEY")


class ApplicationSettings(BaseConfig):
    mode: str = Field(default="dev", alias="MODE")
    cors_origins: list[str] = Field(
        default=["http://localhost:3000"], alias="CORS_ORIGINS"
    )

    database: PostgresSettings = Field(default_factory=PostgresSettings)
    authentication: AuthenticationSettings = Field(
        default_factory=AuthenticationSettings
    )
    minio_config: MinioConfig = Field(default_factory=MinioConfig)
    redis_config: RedisConfig = Field(default_factory=RedisConfig)
    resend_config: ResendSettings = Field(default_factory=ResendSettings)
    sentry_config: SentryConfig = Field(default_factory=SentryConfig)
    kgd_settings: KGDSettings = Field(default_factory=KGDSettings)
    meilisearch_config: MeilisearchConfig = Field(default_factory=MeilisearchConfig)
