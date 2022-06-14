from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    LEVEL: str
    DB_URL: str
    DB_NAME: str
    PROJECT_TITLE: str = "성균관대학교 의상학과 온라인 졸업전시회 API"
    PROJECT_VERSION: int = 1
    PROJECT_DESCRIPTION: str = "성균관대학교 의상학과 온라인 졸업전시회 API"

    class Config:
        env_file = ".env"


class DevelopeSettings(Settings):
    ALLOW_ORIGINS: list[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5500",
        "https://2022skkfdoc.com",
        "https://www.2022skkfdoc.com",
    ]
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: list[str] = ["*"]
    ALLOW_HEADERS: list[str] = ["*"]


class ProductSettings(Settings):
    ALLOW_ORIGINS: list[str] = [
        "https://2022skkfdoc.com",
        "https://www.2022skkfdoc.com",
    ]
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: list[str] = ["*"]
    ALLOW_HEADERS: list[str] = ["*"]


@lru_cache
def get_settings():
    if Settings().LEVEL == "DEVELOP":
        return DevelopeSettings()

    else:
        return ProductSettings()
