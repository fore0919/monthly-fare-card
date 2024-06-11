import os
from typing import Any

import dotenv
from pydantic_settings import BaseSettings

from app.constant.app_env import AppEnv

app_env = os.getenv("APP_ENV", AppEnv.LOCAL)


def get_database() -> dict:
    global app_env
    if app_env == AppEnv.PROD:
        dotenv_file = dotenv.find_dotenv()
        env = dotenv.dotenv_values(dotenv_file)
    else:
        env = {}
    return env


def get_database_uri(env: dict) -> str:
    if not env:
        local_url = os.getenv("DATABASE_URI", "")
        return local_url

    engine = env["engine"]
    password = env["password"]
    host = env["host"]
    dbname = env["dbname"]
    username = env["username"]
    return f"{engine}+aiomysql://{username}:{password}@{host}/{dbname}"


class Settings(BaseSettings):
    model_config = {"case_sensitive": True}

    DB: dict = get_database()
    PROJECT_NAME: str = "monthly-fare-card"
    APP_ENV: AppEnv = AppEnv.LOCAL
    ODSAY_API_KEY: str = (
        os.getenv("ODSAY_API_KEY", "") if AppEnv.LOCAL else DB["ODSAY_API_KEY"]
    )
    HOLIDAY_API_KEY: str = (
        os.getenv("HOLIDAY_API_KEY", "")
        if AppEnv.LOCAL
        else DB["HOLIDAY_API_KEY"]
    )
    SQLALCHEMY_DATABASE_URI: str = get_database_uri(DB)
    SQLALCHEMY_ENGINE_OPTIONS: dict[str, Any] = {"echo": False}
    CORS_ORIGINS: list[str] = ["*"]
    CORS_METHODS: list[str] = [
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "HEAD",
        "OPTIONS",
        "PATCH",
    ]
    CORS_HEADERS: list[str] = [
        "Origin",
        "X-Requested-With",
        "Content-Type",
        "Accept",
        "Content-Disposition",
        "Authorization",
    ]


class Prod(Settings):
    APP_ENV: AppEnv = AppEnv.PROD


def init_settings() -> Settings:
    global app_env
    print(f"env: {app_env}")
    if app_env == AppEnv.PROD:
        return Prod()
    else:
        return Settings()


# ENGINE_CONNECTION_ARGS = get_engine_connection_args()
settings = init_settings()
