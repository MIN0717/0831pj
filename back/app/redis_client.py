import os
from pathlib import Path

from dotenv import load_dotenv
from redis import Redis


# back/.env
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(ENV_PATH)


REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0",
)


redis_client = Redis.from_url(
    REDIS_URL,
    decode_responses=True,
)