import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


class Settings:
    # =========================
    # OpenAI
    # =========================
    OPENAI_API_KEY: str = os.getenv(
        "OPENAI_API_KEY",
        "",
    )

    # =========================
    # AWS
    # =========================
    AWS_ACCESS_KEY_ID: str = os.getenv(
        "AWS_ACCESS_KEY_ID",
        "",
    )

    AWS_SECRET_ACCESS_KEY: str = os.getenv(
        "AWS_SECRET_ACCESS_KEY",
        "",
    )

    AWS_REGION: str = os.getenv(
        "AWS_REGION",
        "ap-northeast-2",
    )

    # =========================
    # S3
    # =========================
    S3_BUCKET_NAME: str = os.getenv(
        "S3_BUCKET_NAME",
        "0831pj-image-rag-data-min0717",
    )

    S3_IMAGE_PREFIX: str = os.getenv(
        "S3_IMAGE_PREFIX",
        "2018-01-011.한국음식이미지_sample",
    )

    # =========================
    # RDS PostgreSQL
    # =========================
    DB_HOST: str = os.getenv(
        "DB_HOST",
        "",
    )

    DB_PORT: int = int(
        os.getenv(
            "DB_PORT",
            "5432",
        )
    )

    DB_NAME: str = os.getenv(
        "DB_NAME",
        "postgres",
    )

    DB_USER: str = os.getenv(
        "DB_USER",
        "postgres",
    )

    DB_PASSWORD: str = os.getenv(
        "DB_PASSWORD",
        "",
    )


settings = Settings()