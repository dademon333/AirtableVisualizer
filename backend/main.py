from fastapi import FastAPI

from api.handlers import api_router
from config import Config

if Config.DEBUG:
    app = FastAPI()
else:
    app = FastAPI(openapi_url=None)

app.include_router(api_router)
