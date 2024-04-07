from utils.logger import configure_logger

logger = configure_logger(__name__)


class FormatRawQueryData:
    def __init__(self):
        self.avg_price_query_keys = ["day", "average_price"]

    def format_avg_price_query_data(self, raw_query_data):
        # Convert list of lists to list of dictionaries
        logger.info("Starting avg price query data formatting")
        list_of_dicts = [dict(zip(self.avg_price_query_keys, row)) for row in raw_query_data]
        logger.info("Completed avg price query data formatting")
        return list_of_dicts
