from fastapi import APIRouter
from .sections import router as sections_router
from .schedule import router as schedule_router

api_router = APIRouter()
api_router.include_router(sections_router)
api_router.include_router(schedule_router)
