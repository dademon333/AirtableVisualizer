from typing import Generic, TypeVar, Type

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """Base for sql CRUD classes with default Create, Read, Update and Delete methods.

        :param model: SQLAlchemy model class
        """
        self.model = model

    # noinspection PyShadowingBuiltins
    async def get_by_id(self, db: AsyncSession, id: int) -> ModelType | None:
        return await db.get(self.model, id)

    async def create(
            self,
            db: AsyncSession,
            create_instance: CreateSchemaType
    ) -> ModelType:
        orm_instance = self.model(**create_instance.dict())
        db.add(orm_instance)
        return orm_instance

    # noinspection PyMethodMayBeStatic
    async def update(
            self,
            db: AsyncSession,
            *,
            orm_instance: ModelType,
            update_instance: UpdateSchemaType
    ) -> ModelType:
        update_instance = update_instance.dict(exclude_unset=True)
        for key, value in update_instance.items():
            setattr(orm_instance, key, value)
        db.add(orm_instance)
        return orm_instance

    # noinspection PyMethodMayBeStatic
    async def remove(self, db: AsyncSession, orm_instance: ModelType) -> None:
        await db.delete(orm_instance)
