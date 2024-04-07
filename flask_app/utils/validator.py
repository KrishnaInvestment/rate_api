import re
from datetime import datetime

from utils.logger import configure_logger
from custom.errors import ValidationError, SQLInjectionError

logger = configure_logger(__name__)

# The logest length of region is 17.
# So aribitrary maximum length
LENGTH_OF_STRING = 25

REGEX_FOR_SQL = r"(\s*([\0\b\'\"\n\r\t\%\_\\]*\s*(((select\s*.+\s*from\s*.+)|(insert\s*.+\s*into\s*.+)|(update\s*.+\s*set\s*.+)|(delete\s*.+\s*from\s*.+)|(drop\s*.+)|(truncate\s*.+)|(alter\s*.+)|(exec\s*.+)|(\s*(all|any|not|and|between|in|like|or|some|contains|containsall|containskey)\s*.+[\=\>\<=\!\~]+.+)|(let\s+.+[\=]\s*.*)|(begin\s*.*\s*end)|(\s*[\/\*]+\s*.*\s*[\*\/]+)|(\s*(\-\-)\s*.*\s+)|(\s*(contains|containsall|containskey)\s+.*)))(\s*[\;]\s*)*)+)"


class Validation:
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

    def detect_sql_injection(self, input_string):
        regex = re.compile(REGEX_FOR_SQL, re.IGNORECASE)
        is_sql = regex.search(input_string)
        if is_sql:
            raise SQLInjectionError("Potential SQL Injection Detected")

    def validate_date(self, value):
        """
        Validates a date string.

        Args:
            value (str): The date string to validate.

        Raises:
            ValueError: If the date string is not in the expected format.
        """
        try:
            datetime.strptime(value, "%Y-%m-%d")
            logger.info(f"Successfully parsed date: {value}")
        except ValueError as e:
            logger.error(f"Failed to parsed date: {value} Error: {e}")
            raise ValueError("Invalid date format. Expected format YYYY-MM-DD")

    def validate_origin_dest(self, value):
        """
        Validates the origin or destination string.

        Args:
            value (str): The origin or destination string to validate.

        Raises:
            ValueError: If the length of the string is more than the specified limit.
        """

        if len(value) >= LENGTH_OF_STRING:
            logger.error(f"Length of {value} is {len(value)}. Expected limit {LENGTH_OF_STRING}")
            raise ValueError(f"The provided string have exceeds length limit of {LENGTH_OF_STRING}")
        else:
            self.detect_sql_injection(value)

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
