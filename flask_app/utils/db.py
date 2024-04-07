import psycopg2
from typing import Any, Tuple
from flask import current_app

from utils.logger import configure_logger
from custom.errors import DBError

logger = configure_logger(__name__)


class DBUtils:
    def __init__(self):
        self.dbms = current_app.config["DBMS"]
        self.db_host = current_app.config["DB_HOST"]
        self.db_port = current_app.config["DB_PORT"]
        self.db_user_name = current_app.config["DB_USER"]
        self.db_password = current_app.config["DB_PASSWORD"]
        self.db_name = current_app.config["DB_NAME"]
        print(current_app.config["DB_NAME"])

    def execute_postgres_query(self, query: str, params: Tuple[Any]):
        """Execute PostGres Query

        query : Raw sql query
        params: Tuple

        Returns:
            Query Result
        """
        conn = psycopg2.connect(
            dbname=self.db_name,
            user=self.db_user_name,
            password=self.db_password,
            host=self.db_host,
        )
        with conn.cursor() as cur:
            # Execute a query
            cur.execute(query, params)
            # logger.info(f'Executed Query {cur.query} query')

            rows = cur.fetchall()
            logger.info(f"Executed Query {rows} query")
            return rows

    def execute_query(self, query, params=None):
        """Factory method for calling the
        appropriate database executing method

        query : Raw sql query
        params: Tuple

        Returns:
            Query Result
        """
        if self.dbms == "POSTGRES":
            logger.info(f"Executing {self.dbms} query")
            return self.execute_postgres_query(query, params)
        else:
            logger.error(f"Provided DBMS {self.dbms} is not valid")
            raise DBError("The selected database type is not valid")


class QueryParamsMaker:
    @staticmethod
    def create_avg_price_query_args(validated_data):
        # Extract region and date parameters from validated data
        origin = validated_data.get("origin")
        destination = validated_data.get("destination")
        date_from = validated_data.get("date_from")
        date_to = validated_data.get("date_to")

        params = [origin, destination, date_from, date_to]

        return params * 2
