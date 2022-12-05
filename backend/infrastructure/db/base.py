import json
from datetime import date, datetime
from typing import Any, AsyncIterator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from config import IS_DEBUG
from tokens import POSTGRESQL_URL


def _json_serializer(obj: Any) -> str | None:
    """Hook for json.dumps to serialize datetime in iso format.

    Usage example:
    data = json.dumps(data, default=json_serializer)

    """
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()


def _json_deserializer(pairs: list[tuple[Any, Any]]) -> dict:
    """Hook for json.loads to deserialize iso format values in datetime.

    Usage example:
    data = json.loads(data, object_pairs_hook=json_deserializer)

    """
    result = {}
    for key, value in pairs:
        if isinstance(value, str):
            try:
                result[key] = datetime.fromisoformat(value)
            except ValueError:
                result[key] = value
        else:
            result[key] = value
    return result


def json_serializer(obj: Any) -> str:
    return json.dumps(
        obj, default=_json_serializer, ensure_ascii=False
    )


def json_deserializer(obj: str) -> dict:
    return json.loads(
        obj, object_pairs_hook=_json_deserializer
    )


def get_enum_values(enum) -> list:
    """Returns a list of enum values.

    Problem: SQLAlchemy uses names of enum's values to store in database
    instead of it's values
    e.g.:
    class UserStatus(enum.Enum):
        USER = 'user'
        MODER = 'moderator'
        ADMIN = 'administrator'
    will be converted to ['USER', 'MODER', 'ADMIN']
    Expected: ['user', 'moderator', 'administrator']

    Solution: pass this func to values_callable arg of sqlalchemy.Enum
    class User(Base):
        ...
        status = Column(Enum(UserStatus, values_callable=get_enum_values))
        ...

    https://stackoverflow.com/a/55160320

    """
    return [x.value for x in enum]


naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}


engine = create_async_engine(
    POSTGRESQL_URL,
    future=True,
    echo=IS_DEBUG,
    json_serializer=json_serializer,
    json_deserializer=json_deserializer
)
metadata = MetaData(bind=engine, naming_convention=naming_convention)
Base = declarative_base(metadata=metadata)


def session_factory(expire_on_commit: bool = True) -> AsyncSession:
    return sessionmaker(  # type: ignore
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=expire_on_commit
    )()


async def get_db() -> AsyncIterator[AsyncSession]:
    session = session_factory()
    try:
        yield session
        await session.commit()
    except:
        await session.rollback()
        raise
    finally:
        await session.close()
