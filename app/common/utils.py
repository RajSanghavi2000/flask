from .enum import SchemaKeysEnum
from datetime import datetime
import pytz
from flask import request

__all__ = ['filter_orm_insert_result', 'dto_mapper', 'get_request_payload', 'str_datetime', 'get_timestamp']


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
