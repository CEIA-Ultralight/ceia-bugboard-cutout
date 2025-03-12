from pydantic import BaseModel, HttpUrl
from uuid import UUID

class ImageRequest(BaseModel):
    id: UUID
    photo_url: HttpUrl

    class Config:
        extra = "ignore"