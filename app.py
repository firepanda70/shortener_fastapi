from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException

from scr.core.base import BaseDBModel
from scr.core.db import engine
from scr.routers import main_router
from scr.exceptions import ValidationException


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''
    Creates migrations in DB on app startup
    '''
    async with engine.begin() as conn:
        await conn.run_sync(BaseDBModel.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(main_router)


@app.exception_handler(ValidationException)
async def validation_exception_handler(
    request: Request, exc: ValidationException
):
    raise HTTPException(
        status_code=exc.status_code,
        detail=exc.reason,
    )
