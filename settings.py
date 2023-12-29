from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.development", ".env.secret"),
        env_file_encoding="utf-8",
    )

    persistence_vault: str = "storage"

    site: str
    media_link: str

    db_url_sync: str
    db_url_async: str

    db_url_dump: str
    db_url_dump_async: str

    test_user: str
    user1: str
    user2: str


settings = Settings()
