from pydantic import BaseModel


class ImageSearchResponse(BaseModel):
    food_name: str
    description: str
    images: list[str]