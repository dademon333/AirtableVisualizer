import os
from distutils.util import strtobool


class Config:
    DEBUG = strtobool(os.getenv('DEBUG'))

    GRAPH_FRONT_ROOT = '/frontend/graph/build'
    TABLE_FRONT_ROOT = '/frontend/table/build'
    BACKUPS_FOLDER = '/var/lib/postgres_backups'

    CORS_ALLOWED_ORIGINS_REGEX = r'https?://localhost:[0-9]{1,5}'
