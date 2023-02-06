from fastapi import APIRouter

router = APIRouter()


@router.get("/all")
async def get_all_public_listings():
    return {}


@router.get("/detail")
async def get_detailed_public_listing(uid: str):
    return {}


@router.put("/update_self")
async def update_self_listing():
    return {}
