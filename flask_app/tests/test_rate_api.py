from flask import current_app
import os
import psycopg2
from pathlib import Path
import unittest

from app import create_app
from utils.db import DBUtils
from config import TestConfig


class TestRateAPIResponse(unittest.TestCase):
    """
    Unit tests for API responses with database operations.
    """

    def db_dev_connection(self):
        """
        Establishes a connection to the development database.
        """
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
        )
        return conn

    def db_test_connection(self):
        """
        Establishes a connection to the test database.
        """
        conn = psycopg2.connect(
            dbname=os.getenv("TEST_POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
        )
        return conn

    def create_test_database(self):
        """
        Creates the test database.
        """
        query = f"CREATE DATABASE {current_app.config['DB_NAME']}"
        conn = self.db_dev_connection()
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.close()
        conn.close()

    def drop_test_database(self):
        """
        Drops the test database.
        """
        query = f"DROP DATABASE {current_app.config['DB_NAME']}"
        conn = self.db_dev_connection()
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.close()
        conn.close()

    def load_data(self):
        """
        Loads data into the test database from an SQL file.
        """
        sql_file_path = Path("tests/test_sql.sql")

        # Open and read the SQL file
        with sql_file_path.open(mode="r") as sql_file:
            # Execute the SQL commands in the file
            conn = self.db_test_connection()
            cursor = conn.cursor()
            cursor.execute(sql_file.read())
            conn.commit()
        cursor.close()
        conn.close()

    def setup_method(self, method):
        """
        Setup method to initialize test environment.
        """
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.context = self.app.app_context()
        self.context.push()
        self.create_test_database()
        self.load_data()

    def teardown_method(self, method):
        """
        Teardown method to clean up test environment.
        """
        self.drop_test_database()
        self.context.pop()

    def test_missing_params(self):
        """
        Test if all required params are provided in the request.
        """
        response = self.client.get("rates/?date_from='2024-01-01")
        self.assertEqual(response.status_code, 400)
        message = "Received key and required keys are not matching. Please make sure request contains date_from, date_to, destination, origin."
        self.assertEqual(response.json["message"], message)

    def test_non_validated_date(self):
        """
        Test if the date format is valid.
        """
        url = "rates/?date_from=20-01-03&date_to=2016-01-03&origin=CNSGH&destination=north_europe_main"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        message = "Invalid date format. Expected format YYYY-MM-DD"
        self.assertEqual(response.json["message"], message)

    def test_sql_injection(self):
        """
        Test if SQL injection is prevented.
        """
        url = "rates/?date_from=2023-01-03&date_to=2016-01-03&origin=CNSGH&destination=select slug from regions"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["message"], "Potential SQL Injection Detected")

    def test_table_counts(self):
        """
        Test the counts of tables in the database.
        """
        # Testing Price_detail table count
        price_detail_count = DBUtils().execute_query("SELECT count(*) FROM price_detail;")
        self.assertEqual(price_detail_count[0][0], 18, "Count of price_detail table is not equal")

        # Testing Route table count
        price_detail_count = DBUtils().execute_query(
            "SELECT count(*) FROM route;", "Count of route table is not equal"
        )
        self.assertEqual(price_detail_count[0][0], 4)

        # Testing Region table count
        price_detail_count = DBUtils().execute_query(
            "SELECT count(*) FROM regions;", "Count of regions table is not equal"
        )
        self.assertEqual(price_detail_count[0][0], 9)

    def test_api_response_for_single_day(self):
        """
        Test response for a single day.
        """
        url = "rates/?date_from=2016-01-01&date_to=2016-01-01&origin=CNCWN&destination=NOGJM"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0].get("average_price"), "2144")

    def test_api_response_with_count_less_than_3(self):
        """
        Test response when count is less than 3.
        """
        url = "rates/?date_from=2016-01-01&date_to=2016-01-01&origin=CNYTN&destination=NOFRO"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json[0].get("average_price"))

    def test_api_response_with_main_regions(self):
        """
        Test response with main regions.
        """
        url = "rates/?date_from=2016-01-01&date_to=2016-01-01&origin=china_main&destination=scandinavia"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0].get("average_price"), "2055")

    def test_api_response_in_date_range(self):
        """
        Test response within date range.
        """
        url = "rates/?date_from=2016-01-02&date_to=2016-01-06&origin=china_main&destination=scandinavia"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Sorting with day
        sorted_json = sorted(response.json, key=lambda x: x["day"])

        # 2016-01-02 have 5 prices
        self.assertEqual(sorted_json[0].get("average_price"), "2171")

        # 2016-01-03 - 2016-01-04 Prices are not available
        self.assertIsNone(sorted_json[1].get("average_price"))
        self.assertIsNone(sorted_json[2].get("average_price"))

        # 2016-01-05 have 3 prices
        self.assertEqual(sorted_json[3].get("average_price"), "2066")

        # 2016-01-06 have 2 prices
        self.assertIsNone(sorted_json[4].get("average_price"))
