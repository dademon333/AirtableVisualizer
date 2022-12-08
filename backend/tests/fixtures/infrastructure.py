import copy
from typing import Any, NoReturn, Callable
from unittest.mock import Mock

import alembic.command
import pytest
from alembic.config import Config
from asynctest import CoroutineMock
from fastapi import FastAPI
from httpx import AsyncClient
from redis.asyncio.client import Redis
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, \
    AsyncEngine
from sqlalchemy.orm import sessionmaker, Session

from infrastructure.db import json_serializer, json_deserializer, get_db
from infrastructure.redis_utils import get_redis_client
from tests.utils import get_test_db_url, get_test_db_name


@pytest.fixture()
def redis_mock() -> Mock:
    storage = {}

    def get(key: str) -> Any:
        return storage.get(key)

    def set_(key: str, value: Any, *_, **__) -> NoReturn:
        storage[key] = value

    def delete(key: str) -> NoReturn:
        del storage[key]

    mock = Mock(spec=Redis)
    mock.get = CoroutineMock(side_effect=get)
    mock.set = CoroutineMock(side_effect=set_)
    mock.delete = CoroutineMock(side_effect=delete)

    return mock


def kill_database_connections(session: Session) -> NoReturn:
    """Kills all connections to db.

    Uses before each drop database (or it can raise exception).
    """
    session.execute(
        text(f'''
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname='{get_test_db_name()}'
        ''')
    )


@pytest.fixture(scope='session')
def db_name() -> str:
    return get_test_db_name()


@pytest.fixture(scope='session')
def db_engine() -> AsyncEngine:
    return create_async_engine(
        get_test_db_url(),
        future=True,
        echo=False,
        json_serializer=json_serializer,
        json_deserializer=json_deserializer
    )


@pytest.fixture(scope='session')
def tables(db_name: str) -> NoReturn:
    url = get_test_db_url()
    url = url.replace(f"/{db_name}", "").replace("+asyncpg", "")
    engine = create_engine(url)
    session = sessionmaker(bind=engine)()
    session.connection().connection.set_isolation_level(0)

    try:
        session.execute(text(f'CREATE DATABASE "{db_name}"'))
    except Exception:
        kill_database_connections(session)
        session.execute(text(f'DROP DATABASE "{db_name}"'))
        session.execute(text(f'CREATE DATABASE "{db_name}"'))

    alembic_config = Config("alembic.ini")
    alembic.command.upgrade(alembic_config, "head")


@pytest.fixture()
async def db(tables: None, db_engine: AsyncEngine) -> AsyncSession:
    session: AsyncSession = sessionmaker(  # type: ignore
        bind=db_engine,
        class_=AsyncSession,
    )()
    yield session
    await session.rollback()


@pytest.fixture()
def app() -> FastAPI:
    from main import app
    return app


@pytest.fixture()
def di_override(app: FastAPI) -> Callable[[Any, Any], NoReturn]:
    old_deps = copy.deepcopy(app.dependency_overrides)

    def override(old: Any, new: Any) -> NoReturn:
        app.dependency_overrides[old] = lambda: new

    yield override
    app.dependency_overrides = old_deps


@pytest.fixture()
async def test_client(
        app: FastAPI,
        db: AsyncSession,
        di_override: Callable[[Any, Any], NoReturn]
) -> AsyncClient:
    di_override(get_redis_client, redis_mock)
    di_override(get_db, db)
    async with AsyncClient(
            app=app, base_url='http://0.0.0.0:5000'
    ) as test_client:
        yield test_client
