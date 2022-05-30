import os
from distutils.util import strtobool


class Config:
    DEBUG = strtobool(os.getenv('DEBUG'))

    FRONT_ROOT = '/usr/src/frontend/build'
    BACKUPS_FOLDER = '/var/lib/postgres_backups'

    CORS_ALLOWED_ORIGINS_REGEX = r'https?://localhost:[0-9]{1,5}'
