from fastapi import APIRouter

from stuff_handlers.handlers import stuff_router
from entities_types_connections.handlers import types_connections_router
from users.handlers import users_router

root_router = APIRouter()

root_router.include_router(stuff_router)
root_router.include_router(
    users_router,
    prefix='/users',
    tags=['Users']
)

root_router.include_router(
    types_connections_router,
    prefix='/types_connections',
    tags=['Types connections']
)
