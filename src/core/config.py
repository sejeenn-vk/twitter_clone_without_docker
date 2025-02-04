import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ALLOWED_EXTENSIONS = (
    "png",
    "jpg",
    "jpeg",
    "gif",
)

STATIC_FOLDER = "/usr/share/nginx/static"
IMAGES_FOLDER = os.path.join(STATIC_FOLDER, "images")

API_KEY_DEFAULT = "test"
USER_ID = "id"
NAME = "name"
MODEL = "model"
RESULT_STR = "result"
TEST_USER2 = "Тестовый Пользователь 2"


class DBSettings(BaseSettings):
    db_name: str
    db_user: str
    db_pass: SecretStr
    db_host: str
    db_port: int
    db_echo: bool

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
        password = self.db_pass.get_secret_value()
        return "postgresql+asyncpg://{:s}:{:s}@{:s}:{:d}/{:s}".format(
            self.db_user, password, self.db_host, self.db_port, self.db_name
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".test.env"),
        case_sensitive=False,
    )
    db: DBSettings = DBSettings()


settings = Settings()
