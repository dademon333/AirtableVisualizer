import sqlalchemy.exc
from sqlalchemy import select, bindparam, cast, Enum
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from db import EntitiesTypesConnection
from schemas.entities_types_connections import EntitiesTypesConnectionCreate, \
    EntitiesTypesConnectionUpdate


class CRUDEntitiesTypesConnections(
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

        is_exists = await db.execute(
            select(EntitiesTypesConnection)
            .where(
                (EntitiesTypesConnection.parent_type == create_instance.child_type)
                & (EntitiesTypesConnection.child_type == create_instance.parent_type)
            )
        )
        is_exists = is_exists.unique().first()
        if is_exists:
            raise sqlalchemy.exc.IntegrityError(None, None, None)

        return await super().create(db, create_instance)


    async def create_from_dict(
            self,
            db: AsyncSession,
            create_instance: dict
    ) -> EntitiesTypesConnection:
        """Creates types connection if not exists mirror."""
        await db.connection(execution_options={'isolation_level': 'REPEATABLE READ'})

        parent_type = cast(
            bindparam('parent_type', create_instance['parent_type']),
            Enum(name='entity_type')
        )
        child_type = cast(
            bindparam('child_type', create_instance['child_type']),
            Enum(name='entity_type')
        )

        is_exists = await db.execute(
            select(EntitiesTypesConnection)
            .where(
                (EntitiesTypesConnection.parent_type == child_type)
                & (EntitiesTypesConnection.child_type == parent_type)
            )
        )
        is_exists = is_exists.unique().first()
        if is_exists:
            raise sqlalchemy.exc.IntegrityError(None, None, None)

        return await super().create_from_dict(db, create_instance)


entities_types_connections = CRUDEntitiesTypesConnections(EntitiesTypesConnection)
