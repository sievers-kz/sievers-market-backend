from pydantic import computed_field, Field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
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

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class AuthenticationSettings(BaseSettings):
    secret_key: str = Field(alias="SECRET_KEY")
    algorithm: str = Field(alias="ALGORITHM")
    access_token_lifetime: int = Field(alias="ACCESS_TOKEN_LIFETIME")
    refresh_token_lifetime: int = Field(alias="REFRESH_TOKEN_LIFETIME")
    email_token_lifetime: int = Field(alias="EMAIL_TOKEN_LIFETIME")
    password_reset_token_lifetime: int = Field(alias="PASSWORD_RESET_TOKEN_LIFETIME")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class SendGridSettings(BaseSettings):
    api_key: str = Field(alias="SEND_GRID_API_KEY")
    from_email: str = Field(alias="FROM_EMAIL")
    email_confirmation_template_id: str = Field(alias="EMAIL_CONFIRMATION_TEMPLATE_ID")
    password_reset_template_id: str = Field(alias="PASSWORD_RESET_TEMPLATE_ID")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class MinioConfig(BaseSettings):
    endpoint: str = Field(alias="MINIO_ENDPOINT")
    access_key: str = Field(alias="MINIO_ACCESS_KEY")
    secret_key: str = Field(alias="MINIO_SECRET_KEY")
    bucket_name: str = Field(alias="MINIO_BUCKET_NAME")
    secure_config: bool = Field(alias="MINIO_SECURE_CONFIG")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class RedisConfig(BaseSettings):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT")
    db: int = Field(alias="REDIS_DB")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class ResendSettings(BaseSettings):
    api_key: str = Field(alias="RESEND_API_KEY")
    from_email: str = Field(alias="RESEND_FROM_EMAIL")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class SentryConfig(BaseSettings):
    dsn: str = Field(alias="SENTRY_DSN")
    mode: str = Field(alias="MODE")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class ApplicationSettings(BaseSettings):
    mode: str = Field(alias="MODE")
    database: PostgresSettings = Field(default_factory=PostgresSettings)
    authentication: AuthenticationSettings = Field(default_factory=AuthenticationSettings)
    sendgrid: SendGridSettings = Field(default_factory=SendGridSettings)
    minio_config: MinioConfig = Field(default_factory=MinioConfig)
    redis_config: RedisConfig = Field(default_factory=RedisConfig)
    resend_config: ResendSettings = Field(default_factory=ResendSettings)
    sentry_config: SentryConfig = Field(default_factory=SentryConfig)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding="utf-8")

