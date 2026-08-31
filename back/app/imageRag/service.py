import base64
import json

from openai import OpenAI

from app.config import settings
from app.storage.s3 import s3_storage


client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


def get_food_categories() -> list[str]:
    """
    S3에 저장된 음식 폴더 목록을 가져온다.

    예:
    2018-01-011.한국음식이미지_sample/
        김밥/
        김치찌개/
        갈비탕/
    """

    root_prefix = (
        f"{settings.S3_IMAGE_PREFIX.rstrip('/')}/"
    )

    keys = s3_storage.list_files(
        prefix=root_prefix
    )

    categories: set[str] = set()

    for key in keys:
        if not key.startswith(root_prefix):
            continue

        relative_key = key[
            len(root_prefix):
        ]

        if not relative_key:
            continue

        parts = relative_key.split("/")

        # 첫 번째 경로가 음식 이름
        if parts[0]:
            categories.add(
                parts[0]
            )

    result = sorted(categories)

    if not result:
        raise RuntimeError(
            "S3에서 음식 카테고리를 찾을 수 없습니다."
        )

    return result


def encode_image(
    image_bytes: bytes,
) -> str:
    """
    이미지 bytes를 base64로 변환
    """

    return base64.b64encode(
        image_bytes
    ).decode(
        "utf-8"
    )


def detect_food(
    image_bytes: bytes,
    content_type: str,
) -> dict:
    """
    OpenAI Vision 모델로
    업로드된 음식 이미지를 판별한다.
    """

    categories = get_food_categories()

    category_text = ", ".join(
        categories
    )

    base64_image = encode_image(
        image_bytes
    )

    prompt = f"""
업로드된 음식 이미지를 분석해라.

아래 음식 카테고리 중에서
이미지와 가장 가까운 음식 하나를 선택해라.

음식 카테고리:
{category_text}

반드시 아래 JSON 형식으로만 응답해라.

{{
    "food_name": "음식 이름",
    "description": "판단 이유"
}}

규칙:
1. food_name은 반드시 위 음식 카테고리 중 하나여야 한다.
2. description은 한 문장으로 작성한다.
3. JSON 이외의 설명은 작성하지 않는다.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt,
                    },
                    {
                        "type": "input_image",
                        "image_url": (
                            f"data:{content_type};base64,"
                            f"{base64_image}"
                        ),
                    },
                ],
            }
        ],
    )

    result_text = (
        response.output_text.strip()
    )

    # 혹시 ```json 코드블록으로 반환하면 제거
    if result_text.startswith("```"):
        result_text = (
            result_text
            .replace(
                "```json",
                "",
            )
            .replace(
                "```",
                "",
            )
            .strip()
        )

    try:
        result = json.loads(
            result_text
        )

    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"GPT JSON 파싱 실패: {result_text}"
        ) from e

    food_name = result.get(
        "food_name"
    )

    if food_name not in categories:
        raise ValueError(
            f"GPT가 존재하지 않는 음식 카테고리를 반환했습니다: "
            f"{food_name}"
        )

    return result


def find_food_images(
    food_name: str,
    limit: int = 5,
) -> list[str]:
    """
    S3에서 해당 음식 폴더의 이미지 검색
    """

    prefix = (
        f"{settings.S3_IMAGE_PREFIX.rstrip('/')}/"
        f"{food_name}/"
    )

    keys = s3_storage.list_files(
        prefix=prefix
    )

    allowed_extensions = (
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    )

    image_keys = [
        key
        for key in keys
        if key.lower().endswith(
            allowed_extensions
        )
    ]

    image_keys = sorted(
        image_keys
    )[:limit]

    return [
        s3_storage.generate_presigned_url(
            key=key,
            expires_in=3600,
        )
        for key in image_keys
    ]


def search_similar_food(
    image_bytes: bytes,
    content_type: str,
) -> dict:
    """
    전체 Image RAG Pipeline

    이미지
    → GPT 음식 판별
    → S3 이미지 검색
    → Presigned URL 생성
    → 결과 반환
    """

    food_result = detect_food(
        image_bytes=image_bytes,
        content_type=content_type,
    )

    food_name = food_result[
        "food_name"
    ]

    images = find_food_images(
        food_name=food_name,
        limit=5,
    )

    return {
        "food_name": food_name,
        "description": food_result[
            "description"
        ],
        "images": images,
    }