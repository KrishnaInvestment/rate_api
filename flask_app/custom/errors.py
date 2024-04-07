class DBError(Exception):
    """DB Error"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ValidationError(Exception):
    """Validation Error"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class SQLInjectionError(Exception):
    """Custom exception for SQL injection attempts."""
