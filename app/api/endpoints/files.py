import uuid
from io import BytesIO

from fastapi import APIRouter, Depends, UploadFile, Response

from app.api.deps import get_session
from app.authenticator import Authenticator
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.image import Image
from app.schemas.image import ImageUploadResponseSchema
from app.exceptions import AppError
from app.models.user import User

router = APIRouter()


@router.get("/img/{image_id}")
async def get_image(
    image_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    image_data = await Image.fetch_with_image_id(session, image_id)
    if not image_data:
        raise AppError.IMAGE_NOT_EXISTS_ERROR
    return Response(content=image_data.data, media_type="image/jpeg")


@router.post("/upload", response_model=ImageUploadResponseSchema)
async def upload_image(
    file: UploadFile,
    user: User = Depends(Authenticator.get_current_user),
    session: AsyncSession = Depends(get_session)
):
    if file.content_type != 'image/jpeg':
        raise AppError.WRONG_IMAGE_FORMAT_ERROR
    new_uuid = uuid.uuid4()
    image_data = file.file.read()
    new_image = Image(uuid=new_uuid, data=image_data, user_id=user.user_id)
    res = await new_image.save(session)
    return ImageUploadResponseSchema(image_id=res.uuid)
