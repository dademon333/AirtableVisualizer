from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from config import Config

index_router = APIRouter()

templates = Jinja2Templates(directory=Config.FRONT_ROOT)


@index_router.get('/', response_class=HTMLResponse, include_in_schema=False)
async def connect(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})
