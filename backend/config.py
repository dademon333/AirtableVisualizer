import os
from distutils.util import strtobool

from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = strtobool(os.getenv('DEBUG'))
