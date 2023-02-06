from fastapi import APIRouter

router = APIRouter()


@router.post("/create")
async def auth_create():
    return {}


@router.post("/login")
async def auth_login():
    return {}


@router.get("/info")
async def auth_get_info():
    return {}
