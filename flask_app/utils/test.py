from flask import current_app
from db_engine.db import DB


class TestDBUtils:
    """
    This Class contains the method to create and drop
    test databases
    """

    def create_test_database(self):
        """
        Creates the test database.
        """
        dbname = current_app.config["DB_NAME"]
        query = f"CREATE DATABASE {dbname}"

        conn = DB().get_db_connection(db_name="postgres")

        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute("SELECT oid FROM pg_database WHERE datname = '%s'" % (dbname))
        exists = cursor.fetchone()

        if exists:
            self.drop_test_database()

        cursor.execute(query)
        cursor.close()
        conn.close()

    def drop_test_database(self):
        """
        Drops the test database.
        """
        query = f"DROP DATABASE {current_app.config['DB_NAME']}"
        conn = DB().get_db_connection(db_name="postgres")
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.close()
        conn.close()
