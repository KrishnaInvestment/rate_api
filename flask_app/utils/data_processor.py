from utils.logger import configure_logger

logger = configure_logger(__name__)


class RateAPIDataFormat:
    def __init__(self):
        self.avg_price_query_keys = ["day", "average_price"]

    def format_avg_price_query_data(self, raw_query_data):
        # Convert list of lists to list of dictionaries
        logger.info("Starting avg price query data formatting")
        list_of_dicts = [dict(zip(self.avg_price_query_keys, row)) for row in raw_query_data]
        logger.info("Completed avg price query data formatting")
        return list_of_dicts

    def create_avg_price_query_args(self, validated_data):
        # Extract region and date parameters from validated data
        origin = validated_data.get("origin")
        destination = validated_data.get("destination")
        date_from = validated_data.get("date_from")
        date_to = validated_data.get("date_to")

        params = [origin, destination, date_from, date_to]

        return params * 2
