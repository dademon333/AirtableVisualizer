from fastapi import APIRouter

from entities.handlers import entities_router
from entity_connections.handlers import entity_connection_router

root_router = APIRouter()

root_router.include_router(
    entities_router,
    prefix='/api/entities',
    tags=['Entities'],
)

root_router.include_router(
    entity_connection_router,
    prefix='/api/entity_connections',
    tags=['Entity connections']
)
