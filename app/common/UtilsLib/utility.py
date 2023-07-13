from __future__ import annotations
import json
import logging
import mimetypes
import validators
import os
import random
import re
import string
import jwt
from datetime import datetime, timedelta, date
from json import JSONEncoder
from urllib.parse import urlparse
from uuid import uuid4
from types import SimpleNamespace
import pathlib
import jsonpath
import pytz
import requests
import shortuuid
from dateutil import tz
from jsonpath_ng import parse
from flask import request, has_request_context
from flask_log_request_id import current_request_id
from marshmallow import ValidationError
from num2words import num2words
from dateutil import relativedelta
from validators import ValidationFailure
import decimal

from UtilsLib.constants import (DT_FMT_ymdHMSf, DT_FMT_HMSf, DT_FMT_HM,
                                GCP_STORAGE_HOST_URL, S3_STORAGE_HOST_URL,
                                SMALL_IMAGE_KEY, AZURE_STORAGE_URL,
                                VARIABLE_PREFIX_AND_TYPE_MAPPING,
                                VARIABLE_PREFIX_MATCHING_SEQUENCE,
                                VARIABLE_PATTERNS_TO_BE_REPLACED,
                                NUMERIC_ENGLISH_TO_URDU_MAPPING,
                                NUMERIC_ENGLISH_TO_ARABIC_MAPPING,
                                URDU_NUMERIC_TO_WORD_MAPPING,
                                ARABIC_LANGUAGE_CODE,
                                DT_FMT_Ymd, LOCAL_STORAGE_URL, CONTACT_VARIABLE_PREFIX,
                                NON_CONTACT_VARIABLE_PRE_POST_FIX,
                                NON_CONTACT_VARIABLE_PREFIX_V2, NON_CONTACT_VARIABLE_POSTFIX_V2,
                                VARIABLE_PATTERN_REGEX, ALLOWED_VARIABLE_CHARACTERS, MIMETYPES,
                                FALLBACK_MESSAGE_PATTERN, VARIABLE_PREFIX_AND_TYPE_MAPPINGS,
                                EMAIL_REGEX, PHONE_REGEX, EXTRA, FILE, BEARER, CONTENT_TYPE,
                                AUTHORIZATION, PHONE_NUMBER_ID, D360_API_KEY, ID, MEDIA, TOKEN,
                                MEDIA_IS_NOT_DOWNLOAD, SYSTEM_VARIABLE_FORMAT
                                )
from UtilsLib.enum import (
    SchemaKeysEnum, StorageProvider, FileTypesGroupEnum, ChannelIdEnum,
    WhatsappChannelProviderIdEnum, ChannelNameEnum, WhatsappChannelProviderNameEnum,
    SMSChannelProviderNameEnum, SMSChannelProviderIdEnum, FileTypesEnum,
    ChannelMappingEnum, EsLatestConFieldsPrefix, VariableTypeEnum, VariableFormatEnum, VariableStatusEnum,
    VariableTypeBranchOperatorEnum, CloudUploadMediaURLEnum, ErrorRegexAndResponseEnum, DialogEventType, DialogTypeEnum,
    Dialog360Environments

)
from UtilsLib.exceptions import BadRequestException
from UtilsLib.slack_helper import SlackWeb
from UtilsLib.trigger_rules_validator import (TriggerRulesValidationService, TriggerRulesValidationServiceV2)
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from jwt.exceptions import PyJWTError, DecodeError, InvalidSignatureError
from dateutil.parser import parse as date_parser
from UtilsLib.third_party_api_helper import download_file

__all__ = ['make_dir', 'is_valid_phone', 'is_valid_email', 'is_valid_json',
           'decode_unicode', 'get_unique_key',
           'get_domain_from_url', 'get_timestamp', 'get_utc_timestamp',
           'get_date_range', 'get_datetime_now',
           'get_ip_address', 'get_request_correlation_id', 'str_datetime',
           'str_to_datetime', 'convert_datetime_to_iso',
           'clear_html_tags', 'timezone_converter', 'get_request_user_id',
           'get_request_header_environment_value',
           'configure_hook', 'get_request_payload',
           'storage_provider_host_address', 'get_small_profile_image_url',
           'validate_schema', 'get_current_time_in_integer',
           'get_variable_type', 'get_variable_label_as_per_the_key',
           'slack_post', 'convert_int_to_timestamp',
           'is_success_request', 'get_value_by_json_path', 'get_match_values_for_button',
           'is_valid_json_list', 'slack_post_attachment', 'get_tomorrow_date', 'last_day_of_month',
           'get_next_month_and_year', 'str_to_date', 'get_start_date_and_end_date_adding_monthly_conversation_balance',
           'get_today_date', 'get_start_date_and_end_date_adding_update_subscription_conversation_balance',
           'get_start_date_and_end_date_create_account_adding_conversation_balance', 'get_current_epoch_time',
           'convert_time_into_given_timezone', "get_past_date", "get_current_time_with_specific_year",
           "is_valid_variable", "aes_encryption", "aes_decryption", "unboxing_dto", 'club_file_type',
           'get_mimetype_from_url', 'get_mimetype_from_extension', 'is_valid_url', 'get_extension', 'get_path_from_url',
           'validate_trigger_rules', 'decode_unicode_dict', 'get_filename_from_url', 'get_feature_details',
           'get_whatsapp_twilio_webhook_url', 'get_gupshup_webhook_url',
           'get_360dialog_webhook_url', 'get_unifonic_webhook_url', 'get_channel_provider_webhook',
           'get_provider_id', 'get_file_type_by_mime_type', 'remove_extension_from_file_name',
           'get_sms_twilio_managed_webhook_url', 'slack_block_post', 'get_whatsapp_meta_webhook_url',
           'validate_jwt_token', 'get_global_channel_name_by_id', 'get_value_by_json_path_v2', 'validate_trigger_rules_v2',
           'get_request_headers_dict', 'get_request_json', 'get_request_form', 'get_path_with_query_params_from_url',
           'split_variable_and_fallback_message', 'get_variable_value_with_fallback_message',
           'get_variable_by_pattern', 'VariableValueValidation',
           'is_valid_branch_operator', 'is_valid_variable_pattern', 'get_past_time',
           'prepare_error_response', 'parse_response', 'get_all_nested_error_messages', 'ThirdPartyMediaUpload',
           'get_next_dialog', 'get_360dialog_cloud_webhook_url', 'check_is_single_message_channel', 'is_valid_pattern']


def make_dir(directory_path):
    """
    This method is used to create new directory if it's already not exists

    :param directory_path: Path of new directory
    :return: True
    """

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    return True


def is_valid_phone(phone_number):
    """
    This method is used to validate the phone number

    :param phone_number: Phone number
    :return: Boolean
    """

    match = re.match(r'^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3,4})?[-. )]*(\d{3,4})?[-. ]*(\d{4,6})(?: *x(\d+))?\s*$',
                     phone_number)
    if match is not None:
        return True
    return False


def is_valid_email(email):
    """
    This method is used to validate the email address

    :param email: Email address
    :return: Boolean
    """

    match = re.match(r"(^(\w+([.-]?[!#$%&'*+-/=?^_`{|}~]\w+)*@[a-zA-Z0-9._-]+\.[a-zA-Z]{2,})$)", email)
    if match is None:
        return False
    return True


def is_valid_json(json_str):
    """
    This method is used to check is the request string is valid JSON or not

    :param json_str: Json string
    :return: Boolean
    """

    try:
        if not isinstance(json.loads(json_str), dict):
            return False
    except:
        return False
    return True


def decode_unicode(unicode_string):
    """
    This method is to decode the unicode string

    :param unicode_string: Unicode string
    :return: Decoded string
    """

    return re.sub('[\xc2-\xf4][\x80-\xbf]+', lambda m: m.group(0).encode('latin1').decode('utf8'), unicode_string)


def get_domain_from_url(url):
    """
    This method is used to filter domain from the URL

    :param url: Url
    :return: Domain
    """

    domain_name = '{uri.netloc}'.format(uri=urlparse(url))
    return domain_name if domain_name else url


def get_unique_key():
    """
    This method is ued to get 32 bit unique key
    Steps:
        1. Get current timestamp in "%H%M%S%f" string format
        2. Select random string of 8 char and add with timestamp
        3. Generate 12 bit random string using shortuuid

    :return: 32 bit Unique key
    """

    timestamp = datetime.now().strftime(DT_FMT_HMSf)
    random_str = timestamp + ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(8))
    uuid_str = shortuuid.ShortUUID().random(length=12)
    return '{}{}'.format(uuid_str, random_str)


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


def clear_html_tags(raw_html):
    """
    This method is used to remove html tags from the string

    :param raw_html: Html string
    :return: String
    """

    try:
        cleaner = re.compile('<.*?>')
        clean_text = re.sub(cleaner, '', raw_html)
        return clean_text
    except:
        return raw_html


def get_datetime_now():
    """
    This method is used to get the current datetime

    :return: Current datetime
    """

    return datetime.now()


def get_past_time(hours):
    """
    Returns a datetime object that represents the time a certain number of hours before the current UTC time.

    :return: A datetime object representing the time a certain number of hours before the current UTC time.
    """

    return datetime.utcnow() - timedelta(hours=hours)


def get_timestamp(timezone=pytz.utc):
    """
    This method is used to get current datetime based on the given time zone. Default it's UTC

    :param timezone: Timezone
    :return: Current datetime based on the time zone
    """

    return datetime.now(tz=timezone)


def convert_datetime_to_iso(date_time):
    """
    This method is used to convert datetime to iso format datetime
    :param date_time: Datetime
    :return: ISO format datetime
    """

    return date_time.replace(tzinfo=pytz.utc).isoformat()


def str_datetime(date_time, str_format=DT_FMT_ymdHMSf):
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


def str_to_datetime(date_time, str_format='%Y-%m-%d %H:%M:%S.%f'):
    """
    This method is used to convert string to datetime

    :param date_time: string datetime
    :param str_format: string format
    :return: String to date time
    """

    return datetime.strptime(date_time, str_format)


def get_utc_timestamp(str_format=DT_FMT_ymdHMSf):
    """
    This method is used to get string format UTC timestamp

    :param str_format: string format
    """

    return str_datetime(get_timestamp(), str_format)


def get_date_range(start_date, end_date):
    """
    This method is used to get missing dates between start and end date

    :param start_date: Start date.
    :param end_date: End date

    :return: Date range
    """

    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def timezone_converter(datetime_str, datetime_format=DT_FMT_HM, from_zone='', to_zone='UTC',
                       is_string_input=True):
    """
    This method is used to convert datetime from one timezone to another

    :param datetime_str: datetime
    :param datetime_format: Datetime format
    :param from_zone: From time zone
    :param to_zone: New time zone
    :param is_string_input: Is datetime in string format. Default it's true
    :return: Converted datetime
    """

    from_timezone = tz.gettz(from_zone)
    to_timezone = tz.gettz(to_zone)
    if is_string_input:
        utc = datetime.strptime(datetime_str, datetime_format)
    else:
        utc = datetime_str
    utc = utc.replace(tzinfo=from_timezone)
    return utc.astimezone(to_timezone)


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


def storage_provider_host_address(bucket_name, storage_provider, aws_service_region_name="", filename=''):
    """
    This method is used to host address of the storage provider

    :param bucket_name: Name of the bucket in which file is placed.
    :param storage_provider: Name of the cloud storage provider.
    :param aws_service_region_name: Region name of the AWS service mandatory if storage provider is "s3".
    :param filename: Name of the file.
    :return: host address of the storage provider
    """
    if storage_provider == StorageProvider.S3.value:
        base_url = S3_STORAGE_HOST_URL.format(bucket_name=bucket_name,
                                              region_name=aws_service_region_name)
        return "{}/{}".format(base_url, filename)

    if storage_provider == StorageProvider.GCP.value:
        base_url = GCP_STORAGE_HOST_URL.format(bucket_name=bucket_name)
        return "{}/{}".format(base_url, filename)

    if storage_provider == StorageProvider.LOCAL_STORAGE.value:
        base_url = LOCAL_STORAGE_URL.format(host=os.environ.get("WOTNOT_CORE_SERVER_ADDRESS"))
        return "{}/{}?location={}".format(base_url, filename, bucket_name)

    if storage_provider == StorageProvider.AZURE.value:
        base_url = AZURE_STORAGE_URL.format(account_name=os.environ.get('AZURE_ACCOUNT_NAME'))
        return '{endpoint}/{bucket_name}/{file_name}'. \
            format(endpoint=base_url, bucket_name=bucket_name, file_name=filename)

    return GCP_STORAGE_HOST_URL


def get_small_profile_image_url(filename, bucket_name, storage_provider, aws_service_region_name=""):
    """
    This method is used to get small image URL as per the image name

    :param filename: Name of the file/image.
    :param bucket_name: Name of the bucket in which file is placed.
    :param storage_provider: Name of the cloud storage provider.
    :param aws_service_region_name: Region name of the AWS service mandatory if storage provider is "s3".
    :return: small image URL
    """

    if filename:
        filename = "{small_image_key}{filename}.png".format(small_image_key=SMALL_IMAGE_KEY,
                                                            filename=filename.rsplit('.')[0])
        storage_host_url = storage_provider_host_address(
            bucket_name,
            storage_provider,
            aws_service_region_name,
            filename
        )
        return storage_host_url
    return filename


def validate_schema(schema_class, payload, logger=None):
    """
    This method is used to validate data with the provided schema class.
    :param schema_class: Marshmallow schema class name.
    :param payload: Payload to be validated.
    :param logger: logger object. In case of validation failed logging is happening. (Optional)
    :return: None if schema is getting validated successfully. Otherwise it will raise ValidationError.
    """

    schema = schema_class()
    try:
        schema.load(payload)
    except ValidationError as e:
        if logger:
            logger.info("Error while validating payload. payload={}, Error={}".format(payload, e.messages))
        raise ValidationError(e.messages)


def get_current_time_in_integer():
    """ This method will return current time """
    return int(datetime.utcnow().timestamp() * 1000)


def get_variable_type(variable):
    """
    This method is used to get type of the variable as per the variable prefix pattern.
    :param variable: variable name. (Example: "¿·$user.ipAddress·?")
    :return: Type of the variable. Return blank ("") if variable pattern doesn't match.
    """
    for prefix in VARIABLE_PREFIX_MATCHING_SEQUENCE:
        if variable.startswith(prefix):
            return VARIABLE_PREFIX_AND_TYPE_MAPPING[prefix]
    return ""


def get_variable_label_as_per_the_key(variable_key):
    """
    This method used to return label of the variable.
    :param variable_key: variable key. (Example: "¿·$user.ipAddress·?")
    :return: label of the variable. (Example: "Ip Address")
    """
    # Replace pattern characters
    for pattern in VARIABLE_PATTERNS_TO_BE_REPLACED:
        variable_key = variable_key.replace(pattern, "")

    # Add space before the Capital characters
    variable_key = re.sub(r"(\w)([A-Z])", r"\1 \2", variable_key)

    # Replace underscore with the space
    variable_key = variable_key.replace("_", " ")

    # Make first character capital without changing rest
    if len(variable_key):
        return variable_key[0].upper() + variable_key[1:]
    return ''


def convert_int_to_timestamp(int_timestamp):
    """This method is used to convert integer timestamp value to datetime"""

    return datetime.fromtimestamp(int_timestamp / 1000)


def is_success_request(status_code: int):
    """Checks HTTP status code is success"""
    return 200 <= status_code <= 299


def get_value_by_json_path(payload: dict, path: str):
    """Gets value from json object for given path"""
    results = jsonpath.jsonpath(payload, path)
    if results:
        return results[0]
    return ""


def get_value_by_json_path_v2(payload: dict, path: str):
    """Fetch value from json object for given path (Extended lookup)"""
    jsonpath_expr = parse(path)
    result = [match.value for match in jsonpath_expr.find(payload)]
    if result:
        return result[0] if len(result) == 1 else result
    return ""


def number_in_string(count):
    """ This method is used return the numeric in string
        Like count = 1,
        Then it returns "1"
    """
    return "{}".format(count)


def number_to_word(count):
    """ This method is used to return the numeric in word
         Like count = 1,
        Then it returns "one"
    """
    return num2words(count)


def numeric_in_arabic(count):
    """ This method is used to return the numeric in Arabic langauge """
    return get_urdu_or_arabic_numeric(count, NUMERIC_ENGLISH_TO_ARABIC_MAPPING)


def numeric_to_word_in_arabic(count):
    """ This method is used to return the numeric count in Arabic word """
    return num2words(count, lang=ARABIC_LANGUAGE_CODE)


def numeric_in_urdu(count):
    """ This method is used to return the numeric in Urdu langauge"""
    return get_urdu_or_arabic_numeric(count, NUMERIC_ENGLISH_TO_URDU_MAPPING)


def numeric_to_word_in_urdu(count):
    """ This method is used to return the numeric count in Urdu word """
    return URDU_NUMERIC_TO_WORD_MAPPING.get(str(count), '')


def get_urdu_or_arabic_numeric(english_numeric, mapping_dict):
    """ This method will fetch and return the numeric in mapping langauge """
    if 0 <= english_numeric <= 9:
        return mapping_dict[str(english_numeric)]
    numeric = ''
    for digit in range(len(str(english_numeric))):
        numeric += mapping_dict[str(english_numeric)[digit]]
    return numeric


def get_match_value_list(count):
    """ This method is used return the list of alternative for numeric of integer """
    return [
        number_in_string(count),
        number_to_word(count),
        numeric_in_arabic(count),
        numeric_to_word_in_arabic(count),
        numeric_in_urdu(count),
        numeric_to_word_in_urdu(count)
    ]


def get_match_values_for_button(buttons):
    """ This method will add match_values list in button payload """
    count = 1
    for button in buttons:
        button['match_values'] = get_match_value_list(count)
        button['match_values'].append(button['title'].lower())
        count += 1

    return json.dumps(buttons)


def slack_post(msg, webhook_url):
    slack_web = SlackWeb(webhook_url=webhook_url)
    try:
        slack_web.post_text(msg)

    except Exception:
        logging.error('SlackPostError %s', slack_web.response)
        logging.exception('ErrorSlackPost %s', msg)


def slack_block_post(blocks, webhook_url):
    slack_web = SlackWeb(webhook_url=webhook_url)
    try:
        slack_web.block_post(blocks)

    except Exception:
        logging.error('SlackBlockPostError %s', slack_web.response)
        logging.exception('ErrorSlackPost %s', blocks)


def is_valid_json_list(json_str):
    """
    This method is used to check is the request string is valid JSON or not

    :param json_str: Json string
    :return: Boolean
    """

    try:
        if not isinstance(json.loads(json_str), list):
            return False
    except:
        return False
    return True


def slack_post_attachment(text, attachments, webhook_url):
    """ This method is used to notify attachments in slack post """
    slack_web = SlackWeb(webhook_url=webhook_url)
    try:
        slack_web.post_attachments(text, attachments)

    except (requests.exceptions.RequestException, Exception):
        msg = json.dumps({"text": text, "attachments": attachments})
        logging.error('SlackAttachmentPostError %s', slack_web.response)
        logging.exception('ErrorSlackPost %s', msg)


def get_tomorrow_date():
    today_date = date.today()
    return today_date + relativedelta.relativedelta(days=1)


def get_next_month_and_year(current_year, current_month):
    if current_month == 12:
        return current_year + 1, 1
    return current_year, current_month + 1


def last_day_of_month(month, year):
    last_days = [31, 30, 29, 28]
    for i in last_days:
        try:
            end = datetime(year, month, i)
        except ValueError:
            continue
        else:
            return end.date()
    return None


def str_to_date(_date):
    return datetime.strptime(_date, DT_FMT_Ymd).date()


def get_billing_cycle_date(day, month, year):
    _date = "{}-{}-{}".format(year, month, day)
    try:
        return str_to_date(_date)
    except ValueError:
        return last_day_of_month(month, year)


def get_start_date_and_end_date_adding_monthly_conversation_balance(plans_details, plan_id, renewal_date,
                                                                    subscription_start_at,
                                                                    conversation_balance_start_date):
    start_date = conversation_balance_start_date
    end_date = get_end_date_adding_monthly_conversation_balance(plans_details, plan_id, renewal_date,
                                                                subscription_start_at, conversation_balance_start_date)
    return start_date, end_date


def get_end_date_adding_monthly_conversation_balance(plans_details, plan_id, renewal_date, subscription_start_at,
                                                     conversation_balance_start_date):
    conversation_balance_start_date = str_to_date(conversation_balance_start_date)
    month = conversation_balance_start_date.month
    year = conversation_balance_start_date.year
    year, month = get_next_month_and_year(year, month)
    day = renewal_date.day
    if plans_details[plan_id]['interval'] == "month" and plans_details[plan_id]['is_stripe_plan']:
        day = subscription_start_at.day
    next_month_billing_date = get_billing_cycle_date(day, month, year)
    end_date = next_month_billing_date + relativedelta.relativedelta(days=-1)
    return end_date


def get_today_date():
    return date.today()


def get_previous_date(_date):
    return _date + relativedelta.relativedelta(days=-1)


def convert_unix_time_to_date(timestamp):
    return datetime.utcfromtimestamp(timestamp).date()


def get_start_date_and_end_date_adding_update_subscription_conversation_balance(current_period_start):
    start_date = convert_unix_time_to_date(current_period_start)
    month = start_date.month
    year = start_date.year
    day = start_date.day
    year, month = get_next_month_and_year(year, month)
    next_month_billing_date = get_billing_cycle_date(day, month, year)
    end_date = get_previous_date(next_month_billing_date)
    return start_date, end_date


def get_start_date_and_end_date_create_account_adding_conversation_balance():
    today_date = get_today_date()
    month = today_date.month
    year = today_date.year
    day = today_date.day
    year, month = get_next_month_and_year(year, month)
    next_month_billing_date = get_billing_cycle_date(day, month, year)
    start_date = today_date
    end_date = get_previous_date(next_month_billing_date)
    return start_date, end_date


def get_current_epoch_time():
    return int(datetime.utcnow().timestamp())


def get_current_time_with_specific_year(year):
    """ This method will return current date time with specific year
    @param: year : int
    @return Datetime
    Current datetime = 31-08-2015
    ex. year = 2022
    returns 2022-08-31
    """
    timestamp = datetime.utcnow().replace(year=year)
    return timestamp.strftime(DT_FMT_Ymd)


def convert_time_into_given_timezone(time, timezone):
    return time.astimezone(pytz.timezone(timezone))


def get_past_date(day):
    today = datetime.utcnow().date()
    return today - timedelta(days=day)


def is_variable_in_lowercase_with_valid_characters(variable):
    """ This method is used to check the variable contains valid characters or not """
    if variable:
        return True if re.match(ALLOWED_VARIABLE_CHARACTERS, variable) else False
    return False


def is_valid_variable(variable):
    """This method is used to validate variable
    It will check below conditions
        1. Startswith `#` and ends_with `#`
        2. Startswith `¿·` or Endswith `·?`
        3. Startswith $user.info.
        And variable contains allowed characters only
            1. Allowed Characters:
                i. Alphabet in lowercase only
               ii. Numerical
              iii. Underscore(_)
    It will return False if above conditions not satisfied
    """
    if (
            not (
                    variable.startswith(NON_CONTACT_VARIABLE_PRE_POST_FIX)
                    and variable.endswith(NON_CONTACT_VARIABLE_PRE_POST_FIX)
                    and is_variable_in_lowercase_with_valid_characters(
                        re.sub(VARIABLE_PATTERN_REGEX, '', variable.strip())
                    )
            )
            and not (
                variable.startswith(NON_CONTACT_VARIABLE_PREFIX_V2)
                and variable.endswith(NON_CONTACT_VARIABLE_POSTFIX_V2)
                and is_variable_in_lowercase_with_valid_characters(
                        re.sub(VARIABLE_PATTERN_REGEX, '', variable.strip())
                )
            )
            and not (
                variable.startswith(CONTACT_VARIABLE_PREFIX)
                and is_variable_in_lowercase_with_valid_characters(
                        re.sub(VARIABLE_PATTERN_REGEX, '', variable.strip())
                )
            )
    ):
        return False
    return True


def aes_encryption(plain_text, private_key):
    """Encrypt plain text using the private key"""

    encoded_plain_text = plain_text.encode()
    f = Fernet(private_key)
    return f.encrypt(encoded_plain_text).decode('utf-8')


def aes_decryption(encrypted_text, private_key):
    """Decrypt encrypted text using private key"""

    encoded_encrypted_text = encrypted_text.encode()
    f = Fernet(private_key)
    return f.decrypt(encoded_encrypted_text).decode('utf-8')


class EventEncoder(JSONEncoder):
    """ This class is used to return object dictionary """

    def default(self, o):
        return o.__dict__


def unboxing_dto(payload):
    """ This method is used unbox the DTO payload """
    return json.loads(json.dumps(payload, cls=EventEncoder, ensure_ascii=False))


def club_file_type(mime_type: str):
    """ This method is used to club the mimetype in custom type

    Note: As of now, we have just grouped only IMAGE and VIDEO if type is not IMAGE or DOCUMENT then return document
    """
    try:
        _type = mime_type.split('/')[0].upper()
        if getattr(FileTypesGroupEnum, _type, None):
            return FileTypesGroupEnum.__getitem__(_type).value
        return FileTypesGroupEnum.DOCUMENT.value
    except Exception:
        return ''


def get_file_type_by_mime_type(mime_type: str, default_file_type=FileTypesEnum.DOCUMENT.value):
    _type = mime_type.split('/')[0].upper()
    if getattr(FileTypesEnum, _type, None):
        return FileTypesEnum.__getitem__(_type).value
    return default_file_type


def is_valid_url(url):
    """ This method is used to check the URL is valid or not ? """
    result = validators.url(url)
    if isinstance(result, ValidationFailure):
        return False
    return True


def get_extension(url):
    """ Get extension from the URL """
    return url.split('.')[-1]


def get_mimetype_from_url(url):
    """ Get mimetype from the URL """
    mime_type, _ = mimetypes.guess_type(url)
    return mime_type


def get_mimetype_from_extension(extension):
    """ Get mimetypes from extension """
    return MIMETYPES.get(extension, '')


def decode_unicode_dict(value):
    if not (isinstance(value, str) or isinstance(value, dict) or isinstance(value, list)):
        return value
    if isinstance(value, str):
        return decode_unicode(value)
    if isinstance(value, dict):
        for key, _value in value.items():
            value[key] = decode_unicode_dict(_value)
        return value
    if isinstance(value, list):
        value = [decode_unicode_dict(_value) for _value in value]
        return value


def get_path_from_url(url):
    return urlparse(url).path


def get_path_with_query_params_from_url(url):
    parse = urlparse(url)
    query = parse.query
    return "{0}{1}".format(parse.path, "?{}".format(query) if query else "")


def validate_trigger_rules(bot_ids, channel_id, language_code, web_url, account_timezone, trigger_rules):
    return TriggerRulesValidationService(
        bot_ids, channel_id, language_code, web_url, account_timezone, trigger_rules).do_process()


def validate_trigger_rules_v2(bot_ids, channel_id, language_code, web_url, account_timezone, trigger_rules):
    return TriggerRulesValidationServiceV2(
        bot_ids, channel_id, language_code, web_url, account_timezone, trigger_rules).do_process()


def get_filename_from_url(url):
    """ This method is used to get filename from URL """

    parsed_url = urlparse(url)
    return os.path.basename(parsed_url.path)


def get_feature_details(features, feature):
    """ This method is used get feature details """

    return features.get(feature)


def get_whatsapp_twilio_webhook_url(base_url, webhook_key):
    return "{base_url}/incoming/twilio-message/{webhook_key}".format(base_url=base_url, webhook_key=webhook_key)


def get_gupshup_webhook_url(base_url, webhook_key):
    return "{base_url}/incoming/gupshup-message/{webhook_key}".format(base_url=base_url, webhook_key=webhook_key)


def get_360dialog_webhook_url(base_url, webhook_key):
    return "{base_url}/incoming/360dialog-message/{webhook_key}".format(base_url=base_url, webhook_key=webhook_key)


def get_360dialog_cloud_webhook_url(base_url, webhook_key):
    return "{base_url}/incoming/360dialog-cloud-message/{webhook_key}".format(base_url=base_url, webhook_key=webhook_key)


def get_unifonic_webhook_url(base_url, webhook_key):
    return "{base_url}/incoming/unifonic-message/{webhook_key}".format(base_url=base_url, webhook_key=webhook_key)


def get_whatsapp_meta_webhook_url(base_url, webhook_key):
    return "{base_url}/incoming/whatsapp/meta-message/{webhook_key}".format(base_url=base_url, webhook_key=webhook_key)


def get_sms_twilio_webhook_url(base_url, webhook_key):
    """ This method is used for the WhatsApp Channel only """
    return "{base_url}/incoming/sms/twilio-message/{webhook_key}".format(base_url=base_url, webhook_key=webhook_key)


def get_sms_twilio_managed_webhook_url(base_url, webhook_key):
    """ This method is used for the WhatsApp Channel only """
    return "{base_url}/incoming/sms/twilio-managed-message/{webhook_key}".format(base_url=base_url, webhook_key=webhook_key)


def get_sms_tech_alpha_webhook_url(base_url, webhook_key):
    """ This method is used for the SMS Channel only """
    return "{base_url}/incoming/sms/tech-alpha/{webhook_key}".format(base_url=base_url, webhook_key=webhook_key)


def get_channel_provider_webhook(base_url, webhook_key, channel_id, provider_id):
    channel_provider_mapping = {
        ChannelIdEnum.WHATSAPP.value: {
            WhatsappChannelProviderIdEnum.TWILIO.value: get_whatsapp_twilio_webhook_url,
            WhatsappChannelProviderIdEnum.GUPSHUP.value: get_gupshup_webhook_url,
            WhatsappChannelProviderIdEnum.DIALOG360.value: get_360dialog_webhook_url,
            WhatsappChannelProviderIdEnum.UNIFONIC.value: get_unifonic_webhook_url,
            WhatsappChannelProviderIdEnum.META.value: get_whatsapp_meta_webhook_url,
            WhatsappChannelProviderIdEnum.DIALOG360CLOUD.value: get_360dialog_cloud_webhook_url
        },
        ChannelIdEnum.SMS.value: {
            SMSChannelProviderIdEnum.TWILIO.value: get_sms_twilio_webhook_url,
            SMSChannelProviderIdEnum.TWILIO_MANAGED.value: get_sms_twilio_managed_webhook_url,
            SMSChannelProviderIdEnum.TECH_ALPHA.value: get_sms_tech_alpha_webhook_url
        }
    }
    if channel_provider_mapping.get(channel_id) and channel_provider_mapping.get(channel_id).get(provider_id):
        return channel_provider_mapping.get(channel_id).get(provider_id)(base_url, webhook_key)
    return ''


def get_provider_id(channel_id, provider):
    return {
        ChannelIdEnum.WHATSAPP.value: {
            WhatsappChannelProviderNameEnum.TWILIO.value: WhatsappChannelProviderIdEnum.TWILIO.value,
            WhatsappChannelProviderNameEnum.GUPSHUP.value: WhatsappChannelProviderIdEnum.GUPSHUP.value,
            WhatsappChannelProviderNameEnum.DIALOG_360.value: WhatsappChannelProviderIdEnum.DIALOG360.value,
            WhatsappChannelProviderNameEnum.UNIFONIC.value: WhatsappChannelProviderIdEnum.UNIFONIC.value,
            WhatsappChannelProviderNameEnum.META.value: WhatsappChannelProviderIdEnum.META.value,
            WhatsappChannelProviderNameEnum.DIALOG_360_CLOUD.value: WhatsappChannelProviderIdEnum.DIALOG360CLOUD.value
        },
        ChannelIdEnum.SMS.value: {
            SMSChannelProviderNameEnum.TWILIO.value: SMSChannelProviderIdEnum.TWILIO.value,
            SMSChannelProviderNameEnum.TWILIO_MANAGED.value: SMSChannelProviderIdEnum.TWILIO_MANAGED.value,
            SMSChannelProviderNameEnum.TECH_ALPHA.value: SMSChannelProviderIdEnum.TECH_ALPHA.value
        }
    }.get(channel_id, {}).get(provider)


def remove_extension_from_file_name(_file_name):
    return _file_name.split(".")[0] if _file_name else ''


def validate_jwt_token(token, secret_key, algorithm, logger):
    payload = {}
    is_valid_token = False
    try:
        payload = jwt.decode(jwt=token, key=secret_key, algorithms=[algorithm])
        is_valid_token = True
    except Exception as e:
        logger.info("ERROR while verifying JWT token: {e}".format(e=e))
    return is_valid_token, payload


def get_global_channel_name_by_id(channel_id):
    """ This method is used to get global channel name by channel ID """
    return ChannelMappingEnum.ID_TO_GLOBAL_NAME.value.get(channel_id, '')


def split_variable_and_fallback_message(variable_with_fallback_message):
    variable = variable_with_fallback_message
    fallback_message = ''
    pattern = fr"{FALLBACK_MESSAGE_PATTERN}.*{FALLBACK_MESSAGE_PATTERN}"
    fallback_message_list = list(set(re.findall(pattern, variable_with_fallback_message)))
    if fallback_message_list:
        fallback_message_with_pattern = fallback_message_list[0]
        variable = variable_with_fallback_message.replace(fallback_message_with_pattern, '')
        fallback_message = fallback_message_with_pattern.replace(FALLBACK_MESSAGE_PATTERN, '')
    return variable, fallback_message


def get_variable_value_with_fallback_message(variables: dict, variable: str, fallback_message: str,
                                             account_variables: dict):
    """ This method is used to get variable value from SimpleNamespace
    It will return fallback message string if there is no variable in SimpleNamespace OR value is empty
    """

    variable_format = account_variables.get(variable, {}).get('format', 'text')
    if variable_format in [VariableFormatEnum.BOOLEAN.value, VariableFormatEnum.NUMBER.value]:
        if variables.get(variable) and variables.get(variable).value is not None:
            if isinstance(variables.get(variable).value, str):
                return variables.get(variable).value
            return json.dumps(variables.get(variable).value)
        return fallback_message
    elif variable_format in [VariableFormatEnum.DATE.value]:
        try:
            value = datetime.fromisoformat(variables.get(variable).value)
            if not (value.hour or value.minute or value.second or value.microsecond):
                return value.strftime('%d-%b-%Y')
            return value.strftime('%d-%b-%Y %I:%M %p')
        except:
            return fallback_message

    if variables.get(variable) and isinstance(variables.get(variable).value, str) and variables.get(variable).value:
        return variables.get(variable).value
    elif variables.get(variable) and isinstance(variables.get(variable).value, SimpleNamespace) and variables.get(
            variable).value:
        return json.loads(json.dumps(variables.get(variable).value, default=lambda s: vars(s)))
    else:
        return fallback_message


def get_variable_by_pattern(variable):
    """
    This method is used to get type of the variable as per the variable prefix pattern.
    :param variable: variable name. (Example: "¿·$user.ipAddress·?")
    :return: Type of the variable. Return blank ("") if variable pattern doesn't match.
    """

    _type = ""
    is_variable = False
    for prefix in VARIABLE_PREFIX_MATCHING_SEQUENCE:
        if variable.startswith(prefix):
            _type = VARIABLE_PREFIX_AND_TYPE_MAPPINGS[prefix]
            break
    for pattern in VARIABLE_PATTERNS_TO_BE_REPLACED:
        variable = variable.replace(pattern, "")
    name = variable
    if name and _type and is_variable_in_lowercase_with_valid_characters(name):
        is_variable = True
    return is_variable, name, _type


def is_valid_pattern(text, regex_pattern):
    """ This method is used to check the regex pattern with the text """
    match = re.match(regex_pattern, text)
    return False if match is None else True


def is_valid_branch_operator(_format, operator):
    def _get_condition_based_on_format():
        return {
            VariableFormatEnum.TEXT.value: VariableTypeBranchOperatorEnum.TEXT.value,
            VariableFormatEnum.NAME.value: VariableTypeBranchOperatorEnum.NAME.value,
            VariableFormatEnum.EMAIL.value: VariableTypeBranchOperatorEnum.EMAIL.value,
            VariableFormatEnum.PHONE.value: VariableTypeBranchOperatorEnum.PHONE.value,
            VariableFormatEnum.REGEX.value: VariableTypeBranchOperatorEnum.REGEX.value,
            VariableFormatEnum.NUMBER.value: VariableTypeBranchOperatorEnum.NUMBER.value,
            VariableFormatEnum.DATE.value: VariableTypeBranchOperatorEnum.DATE.value,
            VariableFormatEnum.BOOLEAN.value: VariableTypeBranchOperatorEnum.BOOLEAN.value
        }.get(_format, {})

    return operator in _get_condition_based_on_format()


class VariableValueValidation:
    def __init__(self, value, _format, status, variable_name, validation=None, is_check_status=True,
                 convert_into_original_type=False, exclude_variables_list=None):
        if exclude_variables_list is None:
            exclude_variables_list = []
        self.exclude_variables_list = exclude_variables_list
        self.format = _format
        self.value = value
        self.status = status
        self.variable_name = variable_name
        self.is_check_status = is_check_status
        self.convert_into_original_type = convert_into_original_type
        self.validation = validation if validation else {}

    def get_function(self):
        return {
            VariableFormatEnum.TEXT.value: self._text,
            VariableFormatEnum.NAME.value: self._name,
            VariableFormatEnum.EMAIL.value: self._email,
            VariableFormatEnum.PHONE.value: self._phone,
            VariableFormatEnum.REGEX.value: self._regex,
            VariableFormatEnum.NUMBER.value: self._number,
            VariableFormatEnum.DATE.value: self._date,
            VariableFormatEnum.BOOLEAN.value: self._boolean
        }.get(self.format)

    def do_process(self):

        if self.variable_name in self.exclude_variables_list:
            return False, self.value

        if not self._is_valid_status():
            return False, self.value
        func = self.get_function()
        if func:
            return func()
        return False, self.value

    def _is_valid_status(self):
        if self.is_check_status:
            return self.status == VariableStatusEnum.ACTIVE.value
        return True

    def __is_string(self):
        return isinstance(self.value, str)

    def __is_integer(self):
        return isinstance(self.value, int)

    def __is_float(self):
        return isinstance(self.value, float)

    def _text(self):
        is_string = self.__is_string()
        if not is_string:
            self.value = json.dumps(self.value)
        is_valid = True
        return is_valid, self.value

    def _name(self):
        return self._text()

    def _phone(self):
        is_text, self.value = self._text()
        is_valid = is_text and is_valid_pattern(self.value, PHONE_REGEX)
        return is_valid, self.value

    def _email(self):
        is_text, self.value = self._text()
        is_valid = is_text and is_valid_pattern(self.value, EMAIL_REGEX)
        return is_valid, self.value

    def _regex(self):
        is_text, self.value = self._text()
        return is_text and is_valid_pattern(self.value, self.validation['regex']), self.value

    def _number(self):
        if self.__is_integer() or self.__is_float():
            if self.convert_into_original_type:
                return True, decimal.Decimal(self.value)
            return True, str(self.value)
        elif self.__is_string():
            try:
                value = decimal.Decimal(self.value)
                if self.convert_into_original_type:
                    return True, value
                return True, self.value
            except:
                return False, self.value
        return False, self.value

    def _date(self):
        try:
            return True, date_parser(self.value).replace(tzinfo=None)
        except:
            return False, self.value

    def _boolean(self):
        self.value = self.value.lower() if self.__is_string() else self.value
        original_value = self._get_original_value()
        return isinstance(original_value, bool), original_value

    def _get_original_value(self):
        try:
            return json.loads(self.value)
        except:
            return self.value


def is_valid_variable_pattern(variable):
    if isinstance(variable, str):
        for prefix in VARIABLE_PREFIX_MATCHING_SEQUENCE:
            if variable.startswith(prefix) and variable.endswith("·?"):
                return True
    return False


class ThirdPartyMediaUpload:
    """
        This class is used to upload media using url and store in
        Meta or 360dialog cloud and generate media_id
    """
    __slots__ = ("url", "auth_details", "channel_provider_id", "logger")

    def __init__(self, url: str, configuration: dict, channel_provider_id: int, logger):
        self.url = url
        self.auth_details = configuration
        self.channel_provider_id = channel_provider_id
        self.logger = logger

    def upload_to_cloud(self):
        try:
            content, status = download_file(self.url, {}, 120, None)
            if is_success_request(status):
                cloud_media_url, headers = self.__get_provider_api()
                with requests.Session() as session:
                    files, data = ThirdPartyMediaUpload.__files_upload_payload(self.channel_provider_id, self.url, content)
                    response = session.post(cloud_media_url,
                                            files=files, data=data, headers=headers)
                if is_success_request(response.status_code):
                    return ThirdPartyMediaUpload.__parse_api_response(response.json()), response.status_code
                else:
                    return response.json(), response.status_code
            else:
                return MEDIA_IS_NOT_DOWNLOAD, status
        except Exception as e:
            self.logger.info(f"Error in ThirdPartyMediaUpload: {self.url}, {self.channel_provider_id}, error: {e}")
            return MEDIA_IS_NOT_DOWNLOAD, 500

    @staticmethod
    def __files_upload_payload(channel_provider_id: int, url: str, content: bytes):
        filename, media_mime_type = ThirdPartyMediaUpload.__file_details(url)
        return {
            WhatsappChannelProviderIdEnum.DIALOG360.value: (None, content),
            WhatsappChannelProviderIdEnum.META.value: (
                [
                    (FILE, (filename, content, media_mime_type))
                ],
                None
            ),
            WhatsappChannelProviderIdEnum.DIALOG360CLOUD.value: (
                [
                    (FILE, (filename, content, media_mime_type))
                ],
                {"messaging_product": "whatsapp"}
            )
        }.get(channel_provider_id)

    def __get_provider_api(self):
        """ This method is used to get channel provider api """
        header = self.__get_header()
        return {
            WhatsappChannelProviderIdEnum.DIALOG360.value: (
                CloudUploadMediaURLEnum.DIALOG360.value, header
            ),
            WhatsappChannelProviderIdEnum.META.value: (
                CloudUploadMediaURLEnum.META.value.format(self.auth_details[EXTRA].get(PHONE_NUMBER_ID, '')), header
            ),
            WhatsappChannelProviderIdEnum.DIALOG360CLOUD.value: (
                CloudUploadMediaURLEnum.DIALOG360CLOUD.value, header
            )
        }.get(self.channel_provider_id)

    def __get_header(self) -> dict:
        token = self.auth_details[TOKEN]
        return {
            WhatsappChannelProviderIdEnum.META.value: {
                AUTHORIZATION: BEARER.format(token),
            },
            WhatsappChannelProviderIdEnum.DIALOG360.value: {
                D360_API_KEY: token,
                CONTENT_TYPE: get_mimetype_from_url(self.url)
            },
            WhatsappChannelProviderIdEnum.DIALOG360CLOUD.value: {
                D360_API_KEY: token
            }
        }.get(self.channel_provider_id)

    @staticmethod
    def __file_details(url: str):
        return pathlib.Path(url).name, get_mimetype_from_url(url)

    @staticmethod
    def __parse_api_response(response: dict):
        return response.get(ID) if ID in response else response.get(MEDIA, [{}]).pop().get(ID)



def prepare_error_response(messages):
    exceptions = []
    for field, error_messages in messages.items():
        if type(error_messages) != list:
            exceptions.extend(find_nested_items(field, error_messages))
        else:
            for error_message in error_messages:
                payload = check_error_and_prepare_payload(field, error_message)
                exceptions.append(payload)
    return exceptions


def find_nested_items(field, error_messages):
    exceptions = []
    for nested_field, nested_error_messages in error_messages.items():
        if type(nested_field) == int:
            nested_field = "[" + str(nested_field) + "]"
            all_fields = field + nested_field
        else:
            all_fields = field + "." + nested_field
        if type(nested_error_messages) == dict:
            exceptions.extend(find_nested_items(all_fields, nested_error_messages))
        else:
            for nested_error_message in nested_error_messages:
                payload = check_error_and_prepare_payload(all_fields, nested_error_message)
                exceptions.append(payload)
    return exceptions


def parse_response(exceptions):
    errors = []
    for exception in exceptions:
        error_data = {"code": exception.code, "payload": exception.payload}
        message = exception.message
        for count in range(1, len(exception.payload)+1):
            variable_name = f"var{count}"
            variable_value = error_data["payload"].get(variable_name)
            message = message.replace("{"+variable_name+"}", variable_value)
        error_data["message"] = message
        errors.append(error_data)
    return {
        'ok': False,
        'errors': errors
    }


def check_error_and_prepare_payload(field, message):
    for regex_and_response in ErrorRegexAndResponseEnum:
        payload = dict()
        match_data = re.match(regex_and_response.value['regex'], message)
        if match_data:
            payload['code'] = regex_and_response.name
            payload['message'] = regex_and_response.value['message']

            values_payload = {
                "var1": field
            }
            values = match_data.groups()
            if values:
                count = 2
                for value in values:
                    values_payload[f"var{count}"] = value
                    count += 1

            payload['payload'] = values_payload
            return regex_and_response.value['exception'](message=payload['message'], code=payload['code'], payload=payload['payload'])

    return BadRequestException(message=message, code="BAD_REQUEST", payload={"var1": field})


def get_all_nested_error_messages(errors):
    error_messages = []
    if isinstance(errors, str):
        error_messages.append(errors)
    elif isinstance(errors, dict):
        for value in errors.values():
            error_messages.extend(get_all_nested_error_messages(value))
    elif isinstance(errors, list):
        for item in errors:
            error_messages.extend(get_all_nested_error_messages(item))
    return error_messages


def get_supported_dialogs(channel_id, provider_id):
    whatsapp_supported_dialogs = [
        DialogTypeEnum.SEND_MESSAGE.value,
        DialogTypeEnum.NAME.value,
        DialogTypeEnum.EMAIL.value,
        DialogTypeEnum.PHONE.value,
        DialogTypeEnum.TEXT.value,
        DialogTypeEnum.FILE_UPLOAD.value,
        DialogTypeEnum.BUTTON.value,
        DialogTypeEnum.LIST.value
    ]

    supported_dialogs = {
        ChannelIdEnum.WHATSAPP.value: {
            WhatsappChannelProviderIdEnum.DIALOG360.value: whatsapp_supported_dialogs,
            WhatsappChannelProviderIdEnum.META.value: whatsapp_supported_dialogs,
            WhatsappChannelProviderIdEnum.DIALOG360CLOUD.value: whatsapp_supported_dialogs
        }
    }
    return supported_dialogs.get(channel_id, {}).get(provider_id, [])


def check_is_identified_at_least_single_supported_dialog(channel_id, provider_id, events):
    for event in events:
        if event.type in [DialogEventType.MESSAGE.value] and event.data.type in get_supported_dialogs(channel_id, provider_id):
            return True
    return False


def check_is_single_message_channel(channel_id, provider_id, conversation):
    def whatsapp(_provider_id, _conversation):

        def dialog360(_conversation):
            environment = conversation.variables.__dict__.get(SYSTEM_VARIABLE_FORMAT.format(variable_name="environment"))
            if not environment:
                return False
            return environment.value == Dialog360Environments.PRODUCTION.value

        def common(_conversation):
            return True

        _func = {
            WhatsappChannelProviderIdEnum.DIALOG360.value: dialog360,
            WhatsappChannelProviderIdEnum.META.value: common,
            WhatsappChannelProviderIdEnum.DIALOG360CLOUD.value: common
        }.get(_provider_id)

        if _func:
            return _func(_conversation)
        return False
    func = {
        ChannelIdEnum.WHATSAPP.value: whatsapp
    }.get(channel_id)
    if func:
        return func(provider_id, conversation)
    return False


def get_next_dialog(channel_id, provider_id, events, next_dialog_key, conversation):
    is_single_message_channel = check_is_single_message_channel(channel_id, provider_id, conversation)
    if is_single_message_channel:
        is_identified_at_least_single_message = check_is_identified_at_least_single_supported_dialog(channel_id,
                                                                                                     provider_id,
                                                                                                     events)
        if is_identified_at_least_single_message:
            return None
    return next_dialog_key