import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "gif",
}
STATIC_FOLDER = "/usr/share/nginx/static"
IMAGES_FOLDER = os.path.join(STATIC_FOLDER, "images")


class DBSettings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASS: SecretStr
    DB_HOST: str
    DB_PORT: int
    DB_ECHO: bool

    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    model_config = SettingsConfigDict(
        env_file=(".env", ".test.env"),
        env_file_encoding="utf8",
        extra="ignore",
    )

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS.get_secret_value()}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".test.env"),
        case_sensitive=False,
    )
    db: DBSettings = DBSettings()


settings = Settings()
