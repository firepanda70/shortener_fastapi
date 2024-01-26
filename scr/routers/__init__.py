from fastapi.routing import APIRouter

from .api import api_router
from .shortcuter import shortcuter_router

main_router = APIRouter()

main_router.include_router(api_router)
main_router.include_router(shortcuter_router)
