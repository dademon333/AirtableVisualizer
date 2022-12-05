from abc import abstractmethod
from typing import TypeVar, Type, Generic, NoReturn

from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db import Base

ModelType = TypeVar('ModelType', bound=Base)
InsertSchemaType = TypeVar('InsertSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class BaseRepository(Generic[ModelType, InsertSchemaType, UpdateSchemaType]):
    """Base for sql repository classes with default
    Create, Read, Update and Delete methods.

    Generic params:
    * ModelType: SQLAlchemy model class, which extends Base
    * InsertSchemaType: pydantic model with fields to create SQL item
    * UpdateSchemaType: pydantic model with fields to update SQL item

    """
    model: Type[ModelType]

    @property
    @abstractmethod
    def model(self) -> Type[ModelType]:
        ...

    def __init__(self, db: AsyncSession):
        self.db = db

    # noinspection PyShadowingBuiltins
    async def get_by_id(self, id: int) -> ModelType | None:
        return await self.db.get(self.model, id)

    async def get_by_ids(self, ids: list[int]) -> list[ModelType]:
        result = await self.db.scalars(
            select(self.model)
            .where(self.model.id.in_(ids))
            .order_by(self.model.id)
        )
        return result.all()

    async def get_many(
            self,
            limit: int = 100,
            offset: int = 0
    ) -> list[ModelType]:
        result = await self.db.scalars(
            select(self.model)
            .order_by(self.model.id)
            .limit(limit)
            .offset(offset)
        )
        return result.unique().all()

    async def get_all(self) -> list[ModelType]:
        result = await self.db.scalars(
            select(self.model)
            .order_by(self.model.id)
        )
        return result.all()

    async def insert(self, insert_dto: InsertSchemaType) -> ModelType:
        result = await self.db.execute(
            insert(self.model)
            .values(**insert_dto.dict(exclude_unset=True))
            .returning('*')
        )
        return result.one()

    async def bulk_insert(
            self,
            insert_dtos: list[InsertSchemaType]
    ) -> list[ModelType]:
        result = await self.db.execute(
            insert(self.model)
            .values([x.dict(exclude_unset=True) for x in insert_dtos])
            .returning('*')
        )
        return result.all()

    # noinspection PyShadowingBuiltins
    async def update(
            self,
            id: int,
            update_dto: UpdateSchemaType
    ) -> ModelType:
        update_values = update_dto.dict(exclude_unset=True)
        if not update_values:
            return await self.get_by_id(id)

        result = await self.db.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(**update_values)
            .returning('*')
        )
        return result.one()

    # noinspection PyShadowingBuiltins
    async def delete(self, id: int) -> NoReturn:
        await self.db.execute(
            delete(self.model)
            .where(self.model.id == id)
        )
