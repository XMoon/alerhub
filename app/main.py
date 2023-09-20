import logging
from uvicorn.logging import DefaultFormatter
from typing import Optional, Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.modules.AlertHub import AlertHub, AlerHubException

# modules
app = FastAPI()
alerthub = AlertHub()


class Alert(BaseModel):
    body: str
    title: Optional[str] = None
    level: Optional[str] = None
    url: Optional[str] = None
    group: Optional[str] = None


@app.exception_handler(AlerHubException)
async def alerhub_exception_handler(request: Request, exc: AlerHubException):
    return JSONResponse(
        status_code=500,
        content={
            "message": f"Oops! {exc}",
            "type": "AlerHubException",
            "result": "failed",
        },
    )

@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    console_formatter = DefaultFormatter("%(levelprefix)s %(message)s")
    handler.setFormatter(console_formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

@app.post("/alert")
async def alert(alert: Alert) -> Any:
    return alerthub.send(**alert.model_dump())
