import logging
import subprocess
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse

from src.api import api_router
from src.core.config import settings, LOG_FORMAT
from src.shortcut.dependencies import enabled
from src.shortcut.models import Shortcut

logging.basicConfig(level=settings.log_level, format=LOG_FORMAT)


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''
    Creates migrations in DB on app startup
    '''
    subprocess.run(['alembic', 'upgrade', 'head']).check_returncode()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

@app.get('/{id}', include_in_schema=False)
async def redirect_shortcut(shortcut: Shortcut = Depends(enabled)):
    return RedirectResponse(shortcut.url, shortcut.status_code)
