import logging
import sys
import os


def configure_logger(logger_name):

    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Configure FileHandler
    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setLevel(logging.INFO)
    log_format = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s"
    )
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    # Configure StreamHandler (to print logs to console)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(log_format)
    logger.addHandler(stream_handler)

    return logger
