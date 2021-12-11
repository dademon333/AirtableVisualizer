import os

from dotenv import load_dotenv

load_dotenv()


class Tokens:
    AIRTABLE_TOKEN = os.getenv('AIRTABLE_TOKEN')
    AIRTABLE_DATABASE_ID = os.getenv('AIRTABLE_DATABASE_ID')

    PSQL_USER = os.getenv('PSQL_USER')
    PSQL_PASSWORD = os.getenv('PSQL_PASSWORD')
    PSQL_HOST = os.getenv('PSQL_HOST')
    PSQL_PORT = os.getenv('PSQL_PORT')
    PSQL_DATABASE = os.getenv('PSQL_DATABASE')

    REDIS_HOST = os.getenv('REDIS_HOST')
