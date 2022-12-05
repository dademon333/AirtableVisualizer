import os

from tokens import POSTGRESQL_DATABASE, POSTGRESQL_URL


def get_test_db_name() -> str:
    worker_id = os.getenv('PYTEST_XDIST_WORKER')
    if worker_id:
        return f'test_{POSTGRESQL_DATABASE}_{worker_id}'
    else:
        return f'test_{POSTGRESQL_DATABASE}'


def get_test_db_url() -> str:
    return POSTGRESQL_URL.replace(POSTGRESQL_DATABASE, get_test_db_name())
