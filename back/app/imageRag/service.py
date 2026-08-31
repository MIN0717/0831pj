import base64
import json

from openai import OpenAI

from app.config import settings

S3_ROOT_PREFIX = "2018-01-011.한국음식이미지_sample"

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


IMAGE_ROOT = settings.FOOD_IMAGE_DIR


def get_food_categories() -> list[str]:
    """
    음식 데이터셋의 폴더 이름을 가져온다.
    """

    if not IMAGE_ROOT.exists():
        raise FileNotFoundError(
            f"음식 이미지 폴더를 찾을 수 없습니다: {IMAGE_ROOT}"
        )

    return sorted(
        folder.name
        for folder in IMAGE_ROOT.iterdir()
        if folder.is_dir()
    )


def encode_image(image_bytes: bytes) -> str:
    """
    이미지 bytes를 base64 문자열로 변환한다.
    """

    return base64.b64encode(
        image_bytes
    ).decode("utf-8")


def detect_food(
    image_bytes: bytes,
    content_type: str,
) -> dict:
    """
    GPT를 사용해서 이미지 속 음식 종류를 판별한다.
    """

    categories = get_food_categories()

    if not categories:
        raise RuntimeError(
            "음식 카테고리가 존재하지 않습니다."
        )

    base64_image = encode_image(image_bytes)

    category_text = ", ".join(categories)

    prompt = f"""
업로드된 음식 이미지를 분석해라.

아래 음식 카테고리 중 이미지와 가장 가까운 음식 하나를 선택해라.

음식 카테고리:
{category_text}

반드시 JSON 형식으로만 응답해라.

{{
    "food_name": "음식 이름",
    "description": "판단 이유"
}}

규칙:
1. food_name은 반드시 제공된 음식 카테고리 중 하나여야 한다.
2. description은 한 문장으로 작성한다.
"""

    response = client.responses.create(
        model="gpt-5.4-mini",
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

    result_text = response.output_text.strip()

    # 혹시 markdown 코드 블록이 들어왔을 경우 제거
    if result_text.startswith("```"):
        result_text = (
            result_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    result = json.loads(result_text)

    food_name = result.get("food_name")

    if food_name not in categories:
        raise ValueError(
            f"존재하지 않는 음식 카테고리입니다: {food_name}"
        )

    return result


def find_food_images(
    food_name: str,
    limit: int = 5,
) -> list[str]:

    prefix = (
        f"{S3_ROOT_PREFIX}/"
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

    image_keys = image_keys[:limit]

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
    전체 Image RAG 서비스 흐름
    """

    food_result = detect_food(
        image_bytes=image_bytes,
        content_type=content_type,
    )

    food_name = food_result["food_name"]

    images = find_food_images(
        food_name=food_name,
        limit=5,
    )

    return {
        "food_name": food_name,
        "description": food_result["description"],
        "images": images,
    }