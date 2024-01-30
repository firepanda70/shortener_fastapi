import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException

from scr.core.config import settings, LOG_FORMAT
from scr.routers import main_router
from scr.exceptions import ValidationException

logging.basicConfig(level=settings.log_level, format=LOG_FORMAT)


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''
    Creates migrations in DB on app startup
    '''
    os.system('alembic upgrade head')
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
