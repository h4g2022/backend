from app.api.endpoints import auth, example, talent, user
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(example.router, tags=["Example"])
api_router.include_router(auth.router, tags=["Authentication"], prefix="/auth")
api_router.include_router(user.router, tags=["User"], prefix="/user")
api_router.include_router(talent.router, tags=["Talent"], prefix="/talent")
