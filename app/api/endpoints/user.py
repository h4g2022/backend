from fastapi import APIRouter

router = APIRouter()


@router.get("/me")
async def get_current_user():
    return {}


@router.put("/me")
async def update_current_user():
    return {}