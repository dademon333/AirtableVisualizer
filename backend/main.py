from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.handlers import api_router
from index_router import index_router

app = FastAPI()
app.include_router(api_router)
app.include_router(index_router)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origin_regex=r'https?://localhost:[0-9]{1,5}',
    allow_methods=['*'],
    allow_headers=['*'],
)
