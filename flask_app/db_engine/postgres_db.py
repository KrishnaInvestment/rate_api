import psycopg2
from typing import Any, Tuple
from flask import current_app

from utils.logger import configure_logger
from custom.errors import DBError
from db_engine.base_class import DBBaseClass

logger = configure_logger(__name__)


class PostGresDB(DBBaseClass):
    def __init__(self):
        self.dbms = current_app.config["DBMS"]
        self.db_host = current_app.config["DB_HOST"]
        self.db_port = current_app.config["DB_PORT"]
        self.db_user_name = current_app.config["DB_USER"]
        self.db_password = current_app.config["DB_PASSWORD"]
        self.db_name = current_app.config["DB_NAME"]

    def get_db_connection(self, **kwargs):
        """
        Establishes a connection to the development database.
        """
        db_name = kwargs.get("db_name") or self.db_name
        db_host = kwargs.get("db_host") or self.db_host
        db_port = kwargs.get("db_port") or self.db_port
        db_password = kwargs.get("db_password") or self.db_password
        db_user_name = kwargs.get("db_user_name") or self.db_user_name

        conn = psycopg2.connect(
            dbname=db_name, user=db_user_name, password=db_password, host=db_host, port=db_port
        )
        return conn

    def execute_query(self, query: str, params: Tuple[Any] = ()):
        """Execute PostGres Query

        query : Raw sql query
        params: Tuple

        Returns:
            Query Result
        """
        try:
            conn = self.get_db_connection()
            with conn.cursor() as cur:
                # Execute a query
                cur.execute(query, params)

                rows = cur.fetchall()
                logger.info("Successfully Executed Postgres Query")
            conn.close()
            return rows
        except Exception as e:
            logger.error(
                f"Error executing Postgres Query: {query} {params}. Error {e}", exc_info=True
            )
            raise DBError("Failed executing Postgres Query")
