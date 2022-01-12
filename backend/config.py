import os
from distutils.util import strtobool
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = strtobool(os.getenv('DEBUG'))

    PROJECT_ROOT = Path(__file__).parent.resolve()
    FRONT_ROOT = os.path.join(PROJECT_ROOT.parent, 'frontend', 'build')
