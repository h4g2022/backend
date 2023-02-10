import uuid

from pydantic.main import BaseModel


class ImageUploadResponseSchema(BaseModel):
    image_id: uuid.UUID
