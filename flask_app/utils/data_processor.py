from utils.logger import configure_logger

logger = configure_logger(__name__)


class RateAPIDataFormat:
    def __init__(self):
        self.avg_price_query_keys = ["day", "average_price"]

    def format_avg_price_query_data(self, raw_query_data):
        # Convert list of lists to list of dictionaries
        logger.info("Starting avg price query data formatting")
        list_of_dicts = []

        # For checking if there is any price in the queried data
        # If there is no price then returning a appropriote message
        is_price_available = False
        for row in raw_query_data:
            list_of_dicts.append(dict(zip(self.avg_price_query_keys, row)))
            if row[1]:
                is_price_available = True
        logger.info("Completed avg price query data formatting")
        if is_price_available:
            return list_of_dicts
        else:
            return {"message": "Average price is not available for given period and regions"}

    def create_avg_price_query_args(self, validated_data):
        # Extract region and date parameters from validated data
        origin = validated_data.get("origin")
        destination = validated_data.get("destination")
        date_from = validated_data.get("date_from")
        date_to = validated_data.get("date_to")

        params = [origin, destination, date_from, date_to]

        return params * 2
