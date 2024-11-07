import os
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    # App related
    tg_api_server: str = os.getenv("TG_API_SERVER", "http://84.252.132.42")
    bot_token: str = os.getenv("BOT_TOKEN", "xxx")
    chat_id: int | str = os.getenv("CHAT_ID", "1003941009")
    # Databases
    pg_url: str = os.getenv(
        "PG_URL", "postgresql+asyncpg://tldl:crackme@localhost:5432/tldl"
    )
    bucket_name: str = os.getenv("S3_BUCKET", "tldl")
    s3_endpoint: str = os.getenv("S3_ENDPOINT", "https://storage.yandexcloud.net")
    s3_access_key_id: str = os.getenv("S3_ACCESS_KEY_ID", "xxx")
    s3_secret_access_key: str = os.getenv("S3_SECRET_ACCESS_KEY", "xxx")
    # LLMs
    key_ya_gpt: str = os.getenv("KEY_YA_GPT", "xxx")
    folder_ya_gpt: str = os.getenv("FOLDER_YA_GPT", "xxx")
    key_gigachat: str = os.getenv(
        "KEY_GIGACHAT",
        "xxx",
    )
    url_llama: str = os.getenv('URL_LLAMA', "http://localhost:11434")


settings = AppSettings()
