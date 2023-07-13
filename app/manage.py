from flask import Flask
from flask_log_request_id import RequestID
from flask_restful import Api
from UtilsLib import configure_logging, configure_hook

from .config import configure_app
from .common import (errors, APP_NAME, LOG_FOLDER_LOCATION, LOG_FILE_LOCATION)


def create_app():
    """
    Initialize Flask Application. And Configuring the app and services.
    - configure_app(): Add configuration to the app.config
    - configure_logging(): Configure logger
    - RequestID(): Track the request id
    - configure_hook(): Add the logs on request start and end
    """

    app = Flask(__name__)
    configure_app(app)
    configure_logging(app, APP_NAME, LOG_FOLDER_LOCATION, LOG_FILE_LOCATION)
    RequestID(app)
    configure_hook(app)
    return app


def create_api(app):
    """ Initialize Flask RESTful"""
    api = Api(app, prefix="/api", errors=errors)
    return api


def app_init(message_broker, message_broker_connection_pool):
    from .common import QueueEnum
    message_broker.queue_init(message_broker_connection_pool, QueueEnum)
    return True
