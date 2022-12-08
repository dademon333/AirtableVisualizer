import asyncio
import os
from pathlib import Path

import pytest

from fix_backward_compatibility import fix_compatibility

fix_compatibility()

pytest_plugins = [
    'tests.fixtures.auth',
    'tests.fixtures.entities',
    'tests.fixtures.entity_connections',
    'tests.fixtures.entity_type_connections',
    'tests.fixtures.infrastructure',
    'tests.fixtures.users',
]


def pytest_make_parametrize_id(config, val):
    """Crutch, which fixes display of parametrize tests names:
    instead of \u0418\u0432... will be normal names."""
    return repr(val)


@pytest.fixture(autouse=True, scope='session')
def chdir():
    """While running single tests, pycharm sets current working directory
    in test directory. This fixture fixes it."""
    os.chdir(Path(__file__).parent.parent)



@pytest.fixture(scope='session')
def event_loop():
    """Replaces pytest-asyncio 'event_loop' function-scope fixture
    by session-scope variant. This allows to use session-scope async fixtures.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
