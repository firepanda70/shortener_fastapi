from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

from scr.routers import main_router
from scr.core.exceptions import ValidationException

app = FastAPI()
app.include_router(main_router)


@app.exception_handler(ValidationException)
async def validation_exception_handler(
    request: Request, exc: ValidationException
):
    raise HTTPException(
        status_code=exc.status_code,
        detail=exc.reason,
    )
