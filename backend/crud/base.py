from typing import Generic, TypeVar, Type

from pydantic import BaseModel
from sqlalchemy import insert, delete, update, select
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

    async def get_many(
            self,
            db: AsyncSession,
            limit: int = 100,
            offset: int = 0
    ):
        result = await db.scalars(
            select(self.model).
            limit(limit).
            offset(offset).
            order_by(self.model.id)
        )
        return result.all()

    async def create(
            self,
            db: AsyncSession,
            create_instance: CreateSchemaType
    ) -> ModelType:
        result = await db.execute(
            insert(self.model)
            .values(**create_instance.dict())
        )
        return await self.get_by_id(db, result.inserted_primary_key)

    # noinspection PyShadowingBuiltins
    async def update(
            self,
            db: AsyncSession,
            id: int,
            update_instance: UpdateSchemaType
    ) -> ModelType:
        update_values = update_instance.dict(exclude_unset=True)
        if update_values != {}:
            await db.execute(
                update(self.model).
                where(self.model.id == id).
                values(**update_values)
            )
        return await self.get_by_id(db, id)

    # noinspection PyShadowingBuiltins
    async def delete(self, db: AsyncSession, id: int) -> None:
        await db.execute(
            delete(self.model).
            where(self.model.id == id)
        )
