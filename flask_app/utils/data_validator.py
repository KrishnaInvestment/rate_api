import re
from datetime import datetime

from utils.logger import configure_logger
from custom.errors import (
    ValidationError,
    SQLInjectionError,
    DateOrderMismatchedError,
    StringLengthExceedError,
)
from utils.constants import MIN_LENGTH_OF_STRING, MAX_LENGTH_OF_STRING, REGEX_FOR_SQL_INJECTION

logger = configure_logger(__name__)


class Validation:
    def detect_sql_injection(self, input_string):
        regex = re.compile(REGEX_FOR_SQL_INJECTION, re.IGNORECASE)
        is_sql = regex.search(input_string)
        if is_sql:
            raise SQLInjectionError("Potential SQL Injection Detected")

    def _validate_str(self, value, string_min_length, string_max_length, check_sql_injection=True):
        """
        Validates the string value to validate.

        Args:
            value (str): String value to validate.
            string_min_length (int) : The lower length limit of string
            string_max_length (int) : The upper length limit of string
            check_sql_injection (bool) : If its true then check potential sql injection

        Raises:
            ValueError: If the length of the string is more than the specified limit.
        """

        if (string_min_length > len(value)) or (len(value) > string_max_length):
            logger.error(
                f"Length of {value} is {len(value)}. Expected limit is between {string_min_length} and {string_max_length}"
            )
            raise StringLengthExceedError(
                f"The provided string have exceeded length limit. It should be between {string_min_length} and {string_max_length}"
            )
        if check_sql_injection:
            self.detect_sql_injection(value)

    def _validate_date_order(self, start, end, date_format):
        """
        Validate the order of dates
        Args:
            start: Start date string
            end: End date string
            date_format: Date format string
        """
        try:
            start_date = datetime.strptime(start, date_format)
            end_date = datetime.strptime(end, date_format)
        except ValueError as e:
            logger.error(f"Failed to parsed date: start_date {start} and end_date {end} Error: {e}")
            raise e

        if start_date > end_date:
            message = f"Order of start date {start} and end date {end} mismatched"
            logger.error(message)
            raise DateOrderMismatchedError(message)


class RateAPIValidation(Validation):
    def __init__(self):
        """
        Initializes the Validation class with a mapping of validation functions for each parameter.
        """
        self.required_keys = ["date_from", "date_to", "origin", "destination"]

    def validate_rates_args(self, params):
        """
        Validates the input parameters using provided validation functions.

        Args:
            params (dict): A dictionary containing input parameters to be validated.

        Raises:
            ValidationError: If any validation fails.
        """
        # Strip whitespace from keys and values in the params dictionary
        param_data = {key.strip(): value.strip() for key, value in params.items()}

        date_from = param_data.get("date_from")
        date_to = param_data.get("date_to")
        origin = param_data.get("origin")
        destination = param_data.get("destination")

        # Checking if received keys and required keys are matching
        received_keys = sorted(list(param_data.keys()))
        if sorted(self.required_keys) != received_keys:
            raise ValidationError(
                f"Received key and required keys are not matching. Please make sure request contains {', '.join(self.required_keys)}."
            )

        # Validating Date format and order
        try:
            self._validate_date_order(
                param_data.get("date_from"), param_data.get("date_to"), "%Y-%m-%d"
            )
        except DateOrderMismatchedError:
            raise ValidationError(
                f"Order of date_from {date_from} and date_to {date_to} mismatched"
            )
        except ValueError:
            raise ValidationError("Invalid date format. Expected format YYYY-MM-DD")

        # Validating origin/destination strings
        try:
            self._validate_str(origin, MIN_LENGTH_OF_STRING, MAX_LENGTH_OF_STRING)
            self._validate_str(destination, MIN_LENGTH_OF_STRING, MAX_LENGTH_OF_STRING)
        except StringLengthExceedError:
            raise ValidationError("The length of Origin/Dest should be between 5 and 25")
        except SQLInjectionError:
            raise ValidationError("The Value of Origin/Dest have possible SQL injection")

        return param_data
