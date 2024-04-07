from flask import Flask
from typing import Type

from config import Config
from end_points.rates_api import rates_bp


def create_app(config_class: Type[Config] = Config) -> Flask:
    """Create a Flask application.

    This method should be used to
    create different instances of flask application with different
    configurations. Doing this gives us a way to create seperate flask
    application for test, production and deployment.

    :param config_class: Config Class. Falsk + other configurations as class variables.
    :type config_class: Config

    :returns: Flask application instance.
    :rtype: Flask
    """
    app = Flask(__name__)

    # setting config
    app.config.from_object(config_class)
    app.register_blueprint(rates_bp, url_prefix="/rates")
    return app
