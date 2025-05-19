from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import URL


class Settings(BaseSettings):
    """
    Settings for the application.
    """

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    def database_url(self, hide_password: bool = False) -> str:
        """
        Returns the database URL.
        If hide_password is True, the password will be hidden.
        If hide_password is False, the password will be shown.

        Example:
        >>> settings = Settings()
        >>> settings.database_url(hide_password=True)
        'postgresql+asyncpg://user:********@host:5432/db'
        >>> settings.database_url(hide_password=False)
        'postgresql+asyncpg://user:password@host:5432/db'
        """
        return URL.create(
            drivername='postgresql+asyncpg',
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
        ).render_as_string(hide_password=hide_password)


def get_settings() -> Settings:
    return Settings()  # type: ignore
