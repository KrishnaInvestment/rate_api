import re
from datetime import datetime

from utils.logger import configure_logger
from custom.errors import ValidationError, SQLInjectionError
from utils.constants import LENGTH_OF_STRING, REGEX_FOR_SQL_INJECTION

logger = configure_logger(__name__)


class Validation:
    def detect_sql_injection(self, input_string):
        regex = re.compile(REGEX_FOR_SQL_INJECTION, re.IGNORECASE)
        is_sql = regex.search(input_string)
        if is_sql:
            raise SQLInjectionError("Potential SQL Injection Detected")

    def _validate_date(self, value, format="%Y-%m-%d"):
        """
        Validates a date string.

        Args:
            value (str): The date string to validate.
            format (str): Format of the date

        Raises:
            ValueError: If the date string is not in the expected format.
        """
        try:
            datetime.strptime(value, format)
        except ValueError as e:
            logger.error(f"Failed to parsed date: {value} Error: {e}")
            raise e

    def _validate_str(self, value, string_length, check_sql_injection=True):
        """
        Validates the origin or destination string.

        Args:
            value (str): The origin or destination string to validate.
            string_length (int) : The integer limit of string
            check_sql_injection (bool) : If its true then check potential sql injection

        Raises:
            ValueError: If the length of the string is more than the specified limit.
        """

        if len(value) >= string_length:
            logger.error(f"Length of {value} is {len(value)}. Expected limit {string_length}")
            raise ValueError(f"The provided string have exceeds length limit of {string_length}")
        if check_sql_injection:
            self.detect_sql_injection(value)


class RateAPIValidation(Validation):
    def __init__(self):
        """
        Initializes the Validation class with a mapping of validation functions for each parameter.
        """
        self.mapping = {
            "date_from": self.validate_date,
            "date_to": self.validate_date,
            "origin": self.validate_origin_dest,
            "destination": self.validate_origin_dest,
        }

    def validate_date(self, value):
        """
        Validates a date string.

        Args:
            value (str): The date string to validate.

        Raises:
            ValueError: If the date string is not in the expected format.
        """
        try:
            self._validate_date(value, "%Y-%m-%d")
            logger.info(f"Successfully parsed date: {value}")
        except ValueError:
            raise ValueError("Invalid date format. Expected format YYYY-MM-DD")

    def validate_origin_dest(self, value):
        """
        Validates the origin or destination string.

        Args:
            value (str): The origin or destination string to validate.

        Raises:
            ValueError: If the length of the string is more than the specified limit.
        """

        self._validate_str(value, LENGTH_OF_STRING)

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

        required_keys = sorted(list(self.mapping.keys()))
        received_keys = sorted(list(param_data.keys()))
        if required_keys != received_keys:
            raise ValidationError(
                f"Received key and required keys are not matching. Please make sure request contains {', '.join(required_keys)}."
            )

        for key, value in param_data.items():
            try:
                # Get the validation function corresponding to the key from the mapping
                validate_func = self.mapping.get(key)

                if not validate_func:
                    logger.error(f"No validation Method found for {key}")
                    raise ValidationError(f"No validation Method found for key: {key}")

                # Validate the field value using the respective validation function
                logger.info(f"Validating {key} using {validate_func.__name__} method")
                validate_func(value)

            except Exception as e:
                # Log and raise a ValidationError if any validation error occurs
                logger.error(f"Validation error for key {key} and value {value}")
                raise ValidationError(str(e))
        return param_data
