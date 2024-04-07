from flask import Blueprint, request, jsonify

from utils.logger import configure_logger
from utils.db import DBUtils, QueryParamsMaker
from utils.validator import Validation
from utils.data_processsing import FormatRawQueryData
from utils.sql_queries import AVG_PRICE_QUERY

logger = configure_logger(__name__)

rates_bp = Blueprint("rates_bp", __name__)


@rates_bp.route("/")
def get_avg_price_daywise():
    # Extract query parameters

    try:
        validated_data = Validation().validate_rates_args(request.args)
    except Exception as e:
        logger.error(f"Failed to validating data {request.args}")
        return jsonify({"message": str(e)}), 400

    # Format params appropriately
    params = QueryParamsMaker.create_avg_price_query_args(validated_data)

    data = DBUtils().execute_query(AVG_PRICE_QUERY, params)

    final_output = FormatRawQueryData().format_avg_price_query_data(data)
    # print(final_output)
    return jsonify(final_output), 200
