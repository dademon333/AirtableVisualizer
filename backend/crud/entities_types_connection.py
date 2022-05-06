import sqlalchemy.exc
from sqlalchemy import insert, select, bindparam, exists, cast, Enum
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from db import EntitiesTypesConnection
from schemas.entities_types_connection import EntitiesTypesConnectionCreate, \
    EntitiesTypesConnectionUpdate


class CRUDEntitiesTypesConnection(
        CRUDBase[
            EntitiesTypesConnection,
            EntitiesTypesConnectionCreate,
            EntitiesTypesConnectionUpdate
        ]
):
    async def create(
            self,
            db: AsyncSession,
            create_instance: EntitiesTypesConnectionCreate
    ) -> EntitiesTypesConnection:
        """Creates types connection if not exists mirror."""
        await db.connection(execution_options={'isolation_level': 'REPEATABLE READ'})

        parent_type = bindparam('parent_type', create_instance.parent_type)
        child_type = bindparam('child_type', create_instance.child_type)
        parent_column_name = bindparam('parent_column_name', create_instance.parent_column_name)
        child_column_name = bindparam('child_column_name', create_instance.child_column_name)

        result = await db.execute(
            insert(EntitiesTypesConnection)
            .from_select(
                [
                    EntitiesTypesConnection.parent_type,
                    EntitiesTypesConnection.child_type,
                    EntitiesTypesConnection.parent_column_name,
                    EntitiesTypesConnection.child_column_name
                ],
                select(
                    parent_type,
                    child_type,
                    parent_column_name,
                    child_column_name
                )
                .where(
                    ~exists().where(
                        (EntitiesTypesConnection.parent_type == child_type)
                        & (EntitiesTypesConnection.child_type == parent_type)
                    )
                )
            )
            .returning(EntitiesTypesConnection.id)
        )
        # SQLAlchemy's result.inserted_primary_key in some reason does not work with insert().from_select()
        # That's why used returning id and .fetchone()
        new_id = result.fetchone()
        if new_id is None:
            raise sqlalchemy.exc.IntegrityError(None, None, None)
        return await self.get_by_id(db, new_id[0])


    async def create_from_dict(
            self,
            db: AsyncSession,
            create_instance: dict
    ) -> EntitiesTypesConnection:
        """Creates types connection if not exists mirror."""
        await db.connection(execution_options={'isolation_level': 'REPEATABLE READ'})

        id = bindparam('id', create_instance['id'])  # noqa
        parent_type = cast(
            bindparam('parent_type', create_instance['parent_type']),
            Enum(name='entity_type')
        )
        child_type = cast(
            bindparam('child_type', create_instance['child_type']),
            Enum(name='entity_type')
        )
        parent_column_name = bindparam(
            'parent_column_name',
            create_instance['parent_column_name']
        )
        child_column_name = bindparam(
            'child_column_name',
            create_instance['child_column_name']
        )

        result = await db.execute(
            insert(EntitiesTypesConnection)
            .from_select(
                [
                    EntitiesTypesConnection.id,
                    EntitiesTypesConnection.parent_type,
                    EntitiesTypesConnection.child_type,
                    EntitiesTypesConnection.parent_column_name,
                    EntitiesTypesConnection.child_column_name
                ],
                select(
                    id,
                    parent_type,
                    child_type,
                    parent_column_name,
                    child_column_name
                )
                .where(
                    ~exists().where(
                        (EntitiesTypesConnection.parent_type == child_type)
                        & (EntitiesTypesConnection.child_type == parent_type)
                    )
                )
            )
            .returning(EntitiesTypesConnection.id)
        )
        # SQLAlchemy's result.inserted_primary_key in some reason does not work with insert().from_select()
        # That's why used returning id and .fetchone()
        new_id = result.fetchone()
        if new_id is None:
            raise sqlalchemy.exc.IntegrityError(None, None, None)
        return await self.get_by_id(db, new_id[0])


entities_types_connection = CRUDEntitiesTypesConnection(EntitiesTypesConnection)
