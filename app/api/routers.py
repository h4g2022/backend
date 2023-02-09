from app.api.endpoints import auth, example, talent, employer, listing
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(example.router, tags=["Example"])
api_router.include_router(auth.router, tags=["Authentication"], prefix="/auth")
api_router.include_router(talent.router, tags=["Talent"], prefix="/talent")
api_router.include_router(employer.router, tags=["Employer"], prefix="/employer")
api_router.include_router(listing.router, tags=["Listing"], prefix="/listing")
