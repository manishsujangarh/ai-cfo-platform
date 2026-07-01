from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI CFO API"
    app_version: str = "0.1.0"
    debug: bool = False

    database_host: str
    database_port: int
    database_name: str
    database_user: str
    database_password: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()