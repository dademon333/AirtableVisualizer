from fastapi import APIRouter

from entities.handlers import entities_router

root_router = APIRouter()
root_router.include_router(
    entities_router,
    prefix='/api/entities',
    tags=['Entities'],
)
