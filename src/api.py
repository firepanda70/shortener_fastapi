from fastapi import APIRouter

from src.shortcut.routers import shortcut_router


api_router = APIRouter(prefix='/api/v1')
api_router.include_router(shortcut_router, prefix='/shortcut', tags=['shortcut'])
