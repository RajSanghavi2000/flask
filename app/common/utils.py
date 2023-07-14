from .enum import SchemaKeysEnum
from .exceptions import InvalidSQLDataBase
from datetime import datetime
import pytz
import os
from uuid import uuid4
from flask_log_request_id import current_request_id
from flask import request, has_request_context

__all__ = ['filter_orm_insert_result', 'dto_mapper', 'get_request_payload', 'str_datetime', 'get_timestamp',
           'SingletonDecorator', 'get_database_url', 'get_database', 'make_dir', 'get_request_correlation_id',
           'get_request_header_environment_value', 'get_request_user_id', 'get_ip_address', 'configure_hook']


def configure_hook(app):
    """
    Configure hooks to add logs on request start and request end. Will not add logs for the health checkup APIs
    ``/k8/readiness`` and ``/k8/liveness``
    """

    def is_ignore_log():
        """Ignore logs for the health checkup APIs"""

        return request.path not in ('/k8/readiness', '/k8/liveness')

    @app.before_request
    def before_request():
        """Add Request start log at the start of the request"""

        if is_ignore_log():
            app.logger.info('Request-Start')

    @app.teardown_request
    def teardown_request(exc):
        """Add Request end log at the end of the request"""

        if is_ignore_log():
            app.logger.info('Request-End')


def get_ip_address():
    """
    This method is used to get the ip address from the request

    :return: Ip Address
    """

    if has_request_context():
        proxy_ip_key = 'HTTP_X_FORWARDED_FOR'
        ip_address = request.environ[proxy_ip_key] if proxy_ip_key in request.environ else request.remote_addr
        if isinstance(ip_address, str):
            # return last access IP address
            return ip_address.split(',')[-1]


def get_request_user_id():
    """
    This method is used to get the request user id

    If request context(object) is available then it will tries to find user id from the headers.
    And if it's not in headers or request context is not present then it will return '-'.

    """

    if has_request_context():
        return request.headers.get('WT_USER_ID', '-')
    return '-'


def get_request_header_environment_value(field_name):
    """
    This method is used to get the specific field value from the request header environment

    If request context(object) is available then it will tries to find field value from the header environment.
    And if it's not in header environment for the field or request context is not present then it will return '-'.

    """

    if has_request_context():
        return request.headers.environ.get(field_name, '-')
    return '-'


def get_request_correlation_id():
    """
    This method is used to get the request correlation id.

    If request context(object) is available then it will first tries to find correlation_id from the headers.
    And if it's not present in headers then it will use flask ``current_request_id`` method to get correlation_id.

    For request context is not available then it will use ``uuid4`` to generate random 32 bit correlation id.

    :return 36 bit correlation id
    """

    if has_request_context():
        if request.headers.get('WT_CORRELATION_ID', None) is None:
            return current_request_id()
        return request.headers.get('WT_CORRELATION_ID', '-')
    return uuid4().__str__()


def make_dir(directory_path):
    """
    This method is used to create new directory if it's already not exists

    :param directory_path: Path of new directory
    :return: True
    """

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    return True


def get_database_url(database):
    return {
        "MySQL": "mysql+pymysql://{user}:{password}@{host}/{database}"
    }.get(database)


def get_database(database):
    if database:
        if database != "MySQL":
            raise InvalidSQLDataBase("Invalid sql database")
        return database
    return "MySQL"


class SingletonDecorator(object):
    """
    This decorator is used to make sure that there is only one object for requested class. If object is already created
    then it will return same object
    """

    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.cls(*args, **kwargs)
        return self.instance


def get_timestamp(timezone=pytz.utc):
    """
    This method is used to get current datetime based on the given time zone. Default it's UTC

    :param timezone: Timezone
    :return: Current datetime based on the time zone
    """

    return datetime.now(tz=timezone)


def str_datetime(date_time, str_format="%Y-%m-%d %H:%M:%S.%f"):
    """
    This method is used to convert datetime to string
    If we want day, minute or second as decimal number(non zero-padded decimal number) then we have to add 'X'
    in front of expected format code like "X%d-%b-%y, X%I:%M %p". Due to platform dependency we can't use default
    code which is "%#d"-> Windows And "%-d" -> Linux, other os

    :param date_time: Datetime
    :param str_format: String format
    :return: String format datetime
    """

    if date_time and not isinstance(date_time, str):
        return date_time.strftime(str_format).replace('X0', '').replace('X', '')
    return date_time


def filter_orm_insert_result(payload):
    if '_sa_instance_state' in payload:
        del payload['_sa_instance_state']

    return payload


def dto_mapper(schema_class, dto_object):
    return schema_class().load(dto_object.__dict__)


def get_request_payload(schema_key):
    """
    Used to fetch request headers, arguments and JSON based on the schema_key

    :param schema_key: Request schema to validate. i.e headers, arguments, body
    :return: JSON
    """

    return {
        SchemaKeysEnum.HEADER.value: get_request_headers_dict,
        SchemaKeysEnum.ARGUMENTS.value: get_arguments_dict,
        SchemaKeysEnum.JSON.value: get_request_json,
        SchemaKeysEnum.FORM.value: get_request_form,
        SchemaKeysEnum.VIEW_ARGUMENTS.value: get_view_args_dict,
        SchemaKeysEnum.FILES.value: get_request_files
    }.get(schema_key)()


def get_request_headers_dict():
    return dict([(value[0].replace('-', '_').upper(), value[1]) for value in request.headers])


def get_arguments_dict():
    return request.args.to_dict()


def get_request_json():
    return request.json


def get_request_form():
    return request.form


def get_view_args_dict():
    return request.view_args


def get_request_files():
    return request.files
