from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseModel):
    """
    Конфигурация для настройки редиса

    Attributes:
        host (str): Хост редис
        port (int): Порт редис (по дефолту 6379)
        password (SecretStr): Пароль редиса
    """

    host: str
    port: int = Field(default=6379)
    password: SecretStr

    @property
    def url(self) -> str:
        """Url редис"""

        return f"redis://:{self.password.get_secret_value()}@{self.host}:{self.port}"


class DatabaseSettings(BaseModel):
    """
    Конфигурация для настройки базы данных

    Attributes:
        host (str): Хост базы данных
        port (int): Порт базы данных (по дефолту 5432)
        username (str): Имя админа базы данных
        password (SecretStr): Пароль базы данных
        name (str): Имя базы данных
    """

    host: str
    port: int = Field(default=5432)
    username: str
    password: SecretStr
    name: str

    @property
    def url(self) -> str:
        """Url базы данных"""

        return f"postgresql+asyncpg://{self.username}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"


class BotSettings(BaseModel):
    """
    Конфигурация для настройки бота

    Attributes:
        token (SecretStr): Токен от BotFather (обязательно)
        admin_ids (list[int]): Список telegram id админов (по дефолту list)
    """

    token: SecretStr
    admin_ids: list[int] = Field(default_factory=list)


class Settings(BaseSettings):
    """
    Конфигурация для настройки проекта, префикс и назначение разделять __ (пример: DATABASE__PORT, BOT__TOKEN)

    Attributes:
        database: Конфигурация базы данных
        redis: Конфигурация редиса
        bot: Конфигурация бота
    """

    database: DatabaseSettings
    redis: RedisSettings
    bot: BotSettings

    model_config = SettingsConfigDict(
        env_file=".env", env_nested_delimiter="__", env_file_encoding="utf-8"
    )


settings = Settings()
