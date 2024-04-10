from flask import Blueprint, request, jsonify

from utils.logger import configure_logger
from db_engine.db import DB
from utils.data_validator import RateAPIValidation
from utils.data_processor import RateAPIDataFormat
from queries.sql_queries import AVG_PRICE_QUERY

logger = configure_logger(__name__)

rates_bp = Blueprint("rates_bp", __name__)


@rates_bp.route("/")
def get_avg_price_daywise():
    try:
        validated_data = RateAPIValidation().validate_rates_args(request.args)
    except Exception as e:
        logger.error(f"Failed to validate data {request.args} Errors:{e} ")
        return jsonify({"message": str(e)}), 400

    params = RateAPIDataFormat().create_avg_price_query_args(validated_data)
    logger.info(f"Created Params for RateAPI {params}")

    try:
        data = DB().execute_query(AVG_PRICE_QUERY, params)
    except Exception as e:
        logger.error(f"Failed to Execute Query {request.args} Error {e}")
        return jsonify({"message": str(e)}), 400

    is_price_available, final_output = RateAPIDataFormat().format_avg_price_query_data(data)

    # Returning no data if the all average prices is null
    if not is_price_available:
        return (
            jsonify({"message": "Average price is not available for given period and regions"}),
            200,
        )

    return jsonify(final_output), 200
