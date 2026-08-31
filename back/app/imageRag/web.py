from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
)

from app.imageRag.schema import ImageSearchResponse
from app.imageRag.service import search_similar_food


router = APIRouter(
    prefix="/api/image-rag",
    tags=["Image RAG"],
)


@router.post(
    "/search",
    response_model=ImageSearchResponse,
)
async def search_image(
    file: UploadFile = File(...),
):
    if not file.content_type:
        raise HTTPException(
            status_code=400,
            detail="파일 형식을 확인할 수 없습니다.",
        )

    if not file.content_type.startswith(
        "image/"
    ):
        raise HTTPException(
            status_code=400,
            detail="이미지 파일만 업로드할 수 있습니다.",
        )

    try:
        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="빈 이미지 파일입니다.",
            )

        result = search_similar_food(
            image_bytes=image_bytes,
            content_type=file.content_type,
        )

        return ImageSearchResponse(
            **result
        )

    except HTTPException:
        raise

    except Exception as e:
        print(
            "[Image RAG Error]",
            repr(e),
        )

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )