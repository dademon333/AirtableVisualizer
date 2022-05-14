from fastapi import APIRouter

from change_log.handlers import change_log_router
from courses.handlers import courses_router
from entities.handlers import entities_router
from entities_connections.handlers import entities_connections_router
from stuff_handlers.handlers import stuff_router
from entities_types_connections.handlers import types_connections_router
from users.handlers import users_router

root_router = APIRouter()

root_router.include_router(stuff_router)
root_router.include_router(
    users_router,
    prefix='/api/users',
    tags=['Users']
)

root_router.include_router(
    courses_router,
    prefix='/api/courses',
    tags=['Courses']
)

root_router.include_router(
    entities_router,
    prefix='/api/entities',
    tags=['Entities']
)

root_router.include_router(
    entities_connections_router,
    prefix='/api/entities_connections',
    tags=['Entities connections']
)

root_router.include_router(
    types_connections_router,
    prefix='/api/types_connections',
    tags=['Types connections']
)

root_router.include_router(
    change_log_router,
    prefix='/api/change_log',
    tags=['Change Log']
)
