import os
import sys

IS_DEBUG = os.getenv('IS_DEBUG') == 'True'
IS_PYTEST = "pytest" in sys.argv[0] or 'PYTEST_XDIST_WORKER' in os.environ

CORS_ALLOWED_ORIGINS_REGEX = r'https?://localhost:[0-9]{1,5}'
