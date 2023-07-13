import os
from builtins import int
from distutils.util import strtobool


def configure_app(app):
    """Configuring the app config"""

    basic_configuration(app)            # Add Basic configuration
    logger_configuration(app)           # Add logger configuration


def basic_configuration(app):
    """Add Basic configuration to the app config"""

    app.config['ENVIRONMENT'] = os.environ.get("ENVIRONMENT")
    app.config['DEBUG'] = strtobool(os.environ.get("DEBUG", "0"))
    app.config['TESTING'] = strtobool(os.environ.get("TESTING", "0"))
    app.config['PORT'] = int(os.environ.get("MICRO_SERVICE_PORT"))
    app.config['PRODUCT_NAME'] = os.environ.get("PRODUCT_NAME")
    app.config['SERVER_THREAD_POOL'] = int(os.environ.get("SERVER_THREAD_POOL"))
    app.config['SERVER_SHUTDOWN_TIMEOUT'] = int(os.environ.get("SERVER_SHUTDOWN_TIMEOUT"))


def logger_configuration(app):
    """Add logger configuration to the app config"""

    app.config['ENABLE_GRAYLOG'] = int(os.environ.get("ENABLE_GRAYLOG"))
    app.config['GRAYLOG_HOST'] = os.environ.get("GRAYLOG_HOST")
    app.config['GRAYLOG_PORT'] = int(os.environ.get("GRAYLOG_PORT", "12201"))