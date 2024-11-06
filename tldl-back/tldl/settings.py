import os
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    # App related
    bot_token: str = os.getenv(
        "BOT_TOKEN", "7008982832:AAGTOSXd4AY3ZKwdvcnro48lwmxx-ab8pJI"
    )
    chat_id: int | str = os.getenv("CHAT_ID", "1003941009")
    # Databases
    pg_url: str = os.getenv(
        "PG_URL", "postgresql+asyncpg://tldl:crackme@localhost:5432/tldl"
    )
    bucket_name: str = os.getenv("MINIO_BUCKET", "tldl-raw")


settings = AppSettings()