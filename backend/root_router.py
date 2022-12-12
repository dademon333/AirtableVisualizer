from fastapi import APIRouter

from auth.handlers import auth_router
from courses.handlers import courses_router
from entities.handlers import entities_router
from entity_connections.handlers import entity_connections_router
from entity_type_connections.handlers import type_connections_router
from stuff_handlers.handlers import stuff_router

root_router = APIRouter()

root_router.include_router(stuff_router)

root_router.include_router(
    auth_router,
    prefix='/api/auth',
    tags=['Auth'],
)

root_router.include_router(
    entities_router,
    prefix='/api/entities',
    tags=['Entities'],
)

root_router.include_router(
    courses_router,
    prefix='/api/courses',
    tags=['Courses']
)

root_router.include_router(
    type_connections_router,
    prefix='/api/type_connections',
    tags=['Type connections']
)

root_router.include_router(
    entity_connections_router,
    prefix='/api/entity_connections',
    tags=['Entity connections']
)
