import psycopg2
from flask import current_app

from utils.logger import configure_logger
from custom.errors import DBError
from db_engine.postgres_db import PostGresDB

logger = configure_logger(__name__)


class DB(PostGresDB):
    pass
