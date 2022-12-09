from fastapi import APIRouter

from entities.handlers import entities_router
from entity_connections.handlers import entity_connection_router
from entity_type_connections.handlers import type_connections_router

root_router = APIRouter()

root_router.include_router(
    entities_router,
    prefix='/api/entities',
    tags=['Entities'],
)

root_router.include_router(
    type_connections_router,
    prefix='/api/type_connections',
    tags=['Type connections']
)

root_router.include_router(
    entity_connection_router,
    prefix='/api/entity_connections',
    tags=['Entity connections']
)
