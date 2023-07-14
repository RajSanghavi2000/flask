import logging
from pygelf import GelfUdpHandler
from logging.handlers import TimedRotatingFileHandler
from .utils import make_dir, get_request_correlation_id, get_request_header_environment_value, get_request_user_id, \
    get_ip_address

__all__ = ['configure_logging_log_file', 'configure_graylog', 'configure_logging']


def get_http_request_fields(record):
    """This method is used to get required data to add into the log records"""

    record.correlation_id = get_request_correlation_id()
    record.user_id = get_request_user_id()
    record.path_info = get_request_header_environment_value('PATH_INFO')
    record.query_string = get_request_header_environment_value('QUERY_STRING')
    record.method = get_request_header_environment_value('REQUEST_METHOD')
    record.http_origin = get_request_header_environment_value('HTTP_ORIGIN')
    record.ip_address = get_ip_address()
    record.user_agent = get_request_header_environment_value('HTTP_USER_AGENT')
    record.file_path = record.pathname
    return record


class RequestFormatter(logging.Formatter):
    """Use in local logs configuration to filter and format the records"""

    def format(self, record):
        record = get_http_request_fields(record)
        return super().format(record)


class GrayLogContextFilter(logging.Filter):
    """Use in GrayLog configuration to filter and format the records"""

    def filter(self, record):
        get_http_request_fields(record)
        return True


def configure_logging_log_file(app, log_folder_location, log_file_location, log_file_rotating_time,
                               log_interval, log_backup_count):
    """
    Track Logging in Log file.

    Steps to configure the logger
        Step 1: Create log directory if not exits
        Step 2: Set logger level to the info
        Step 3: Set log file path
        Step 4: Configure ``TimeRotatingFileHandler`` to rotating the log file at certain timed intervals
        Step 5: Set handler level to the info
        Step 6: Set log message formatter
        Step 7: Add handler to the app logger

    :param app: Flask APP
    :param log_folder_location: Log folder location
    :param log_file_location: Log file location
    :param log_file_rotating_time: Time to change log file.
    :param log_interval: Log interval.
    :param log_backup_count: Log backup count.
    """

    LOG_FORMAT = '[%(asctime)s] [%(levelname)s] [%(correlation_id)s] [%(method)s] [%(path_info)s] [%(query_string)s] [%(' \
                 'pathname)s] %(funcName)s: %(lineno)d : %(message)s] [%(ip_address)s] [%(http_origin)s] [%(user_agent)s] '

    make_dir(log_folder_location)

    app.logger.setLevel(logging.DEBUG)
    handler = TimedRotatingFileHandler(log_file_location, when=log_file_rotating_time,
                                       interval=log_interval, encoding='utf8', backupCount=log_backup_count)
    handler.setLevel(logging.DEBUG)

    formatter = RequestFormatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)


def configure_graylog(app, app_name):
    """
    Set up the Graylog for log the logs into the Graylog

    Steps to setup the GrayLog:
        Step 1: Setting app, product_name and environment as additional fields
        Step 2: Set app logger level to the info
        Step 3: Use ``GelUdpHandler`` class of package ``pygelf`` to get the GrayLog handler
        Step 4: Set gelf handler to debug true
        Step 5: Set gelf handler level to info
        Step 6: Add context filter to format the log in app logger
        Step 7: Add gelf handle to the app logger

    Required environment variables:
        PRODUCT_NAME: Name of the product
        ENVIRONMENT: Environment where app is running
        GRAYLOG_HOST: Host address of the GrayLog server
        GRAYLOG_PORT: Port number of the GrayLog server

    :param app: Flask APP
    :param app_name: Service name
    """

    additional_fields = {"app": app_name,
                         "facility": app.config['PRODUCT_NAME'],
                         "environment": app.config['ENVIRONMENT']}

    app.logger.setLevel(logging.INFO)
    gelf_upd_handler = GelfUdpHandler(host=app.config["GRAYLOG_HOST"],
                                      port=app.config["GRAYLOG_PORT"],
                                      include_extra_fields=True,
                                      compress=True,
                                      chunk_size=1300,
                                      **additional_fields)

    gelf_upd_handler.debug = True
    gelf_upd_handler.setLevel(logging.DEBUG)
    app.logger.addFilter(GrayLogContextFilter())
    app.logger.addHandler(gelf_upd_handler)


def configure_logging(app, app_name, log_folder_location, log_file_location, log_file_rotating_time='midnight',
                      log_interval=1, log_backup_count=1825):
    """
    Set up the global logging settings. If GrayLog is enable then it will configure graylog for the logs.
    Else it will configure logs file in local

    :param app: Flask APP
    :param app_name: Service name
    :param log_folder_location: Log folder location
    :param log_file_location: Log file location
    :param log_file_rotating_time: Time to change log file. Default it's `midnight`
    :param log_interval: Log interval. Default it's `1`
    :param log_backup_count: Log backup count. Default it's `1825`
    """

    if app.config["ENABLE_GRAYLOG"]:
        configure_graylog(app, app_name)
    else:
        configure_logging_log_file(app, log_folder_location, log_file_location, log_file_rotating_time,
                                   log_interval, log_backup_count)
