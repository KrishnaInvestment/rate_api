from pathlib import Path
import unittest

from app import create_app
from db_engine.db import DB
from config import TestConfig
from utils.test import TestDBUtils


class TestRateAPI(unittest.TestCase, TestDBUtils):
    """
    Unit tests for API responses with database operations.
    """

    def load_rateapi_data(self):
        """
        Loads data into the test database from an SQL file.
        """
        sql_file_path = Path("tests/sql_data/test_sql.sql")

        # Open and read the SQL file
        with sql_file_path.open(mode="r") as sql_file:
            # Execute the SQL commands in the file
            conn = DB().get_db_connection()
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
        self.load_rateapi_data()

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
        message = "Received key and required keys are not matching. Please make sure request contains date_from, date_to, origin, destination."
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

    def test_non_validated_regions(self):
        """
        Test if the date format is valid.
        """
        url = "rates/?date_from=2016-01-03&date_to=2016-01-03&origin=CNSGH&destination="
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        message = "The length of Origin/Dest should be between 5 and 25"
        self.assertEqual(response.json["message"], message)

    def test_sql_injection(self):
        """
        Test if SQL injection is prevented.
        """
        url = "rates/?date_from=2016-01-03&date_to=2016-01-03&origin=CNSGH&destination=select slug from regions"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        message = "The Value of Origin/Dest have possible SQL injection"
        self.assertEqual(response.json["message"], message)

    def test_non_ordered_date(self):
        """
        Test if SQL injection is prevented.
        """
        url = "rates/?date_from=2023-01-03&date_to=2016-01-03&origin=CNSGH&destination=select slug from regions"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        message = "Order of date_from 2023-01-03 and date_to 2016-01-03 mismatched"
        self.assertEqual(response.json["message"], message)

    def test_non_available_regions_data(self):
        """
        Test if SQL injection is prevented.
        """
        url = "rates/?date_from=2016-01-03&date_to=2016-01-03&origin=CNSGH&destination=CNSGH"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        message = "Average price is not available for given period and regions"
        self.assertEqual(response.json["message"], message)

    def test_table_counts(self):
        """
        Test the counts of tables in the database.
        """
        # Testing Price_detail table count
        price_detail_count = DB().execute_query("SELECT count(*) FROM price_detail;")
        self.assertEqual(price_detail_count[0][0], 18, "Count of price_detail table is not equal")

        # Testing Route table count
        price_detail_count = DB().execute_query(
            "SELECT count(*) FROM route;", "Count of route table is not equal"
        )
        self.assertEqual(price_detail_count[0][0], 4)

        # Testing Region table count
        price_detail_count = DB().execute_query(
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
        message = "Average price is not available for given period and regions"
        self.assertEqual(response.json["message"], message)

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
