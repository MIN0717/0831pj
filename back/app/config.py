import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


class Settings:
    # OpenAI
    OPENAI_API_KEY: str = os.getenv(
        "OPENAI_API_KEY",
        "",
    )

    # AWS
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

    AWS_S3_BUCKET_NAME: str = os.getenv(
        "AWS_S3_BUCKET_NAME",
        "",
    )

    # Local Image
    IMAGE_DIR: Path = BASE_DIR / "images"

    @property
    def FOOD_IMAGE_DIR(self) -> Path:
        if not self.IMAGE_DIR.exists():
            raise FileNotFoundError(
                f"이미지 폴더가 없습니다: {self.IMAGE_DIR}"
            )

        folders = [
            path
            for path in self.IMAGE_DIR.iterdir()
            if path.is_dir()
        ]

        if not folders:
            raise FileNotFoundError(
                "images 폴더 안에 음식 데이터셋이 없습니다."
            )

        return folders[0]


settings = Settings()