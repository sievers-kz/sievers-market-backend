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


class ObjectStorageSettings(BaseSettings):
    object_storage_endpoint: str = Field(alias="OBJECT_STORAGE_ENDPOINT")
    object_storage_access_key: str = Field(alias="OBJECT_STORAGE_ACCESS_KEY")
    object_storage_secret_key: str = Field(alias="OBJECT_STORAGE_SECRET_KEY")
    object_storage_bucket_name: str = Field(alias="OBJECT_STORAGE_BUCKET_NAME")
    object_storage_secure_config: bool = Field(alias="OBJECT_STORAGE_SECURE_CONFIG")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class ApplicationSettings(BaseSettings):
    database: PostgresSettings = Field(default_factory=PostgresSettings)
    authentication: AuthenticationSettings = Field(default_factory=AuthenticationSettings)
    sendgrid: SendGridSettings = Field(default_factory=SendGridSettings)
    object_storage: ObjectStorageSettings = Field(default_factory=ObjectStorageSettings)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding="utf-8")

