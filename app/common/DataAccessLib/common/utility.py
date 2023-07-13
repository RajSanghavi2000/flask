import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


from DataAccessLib.common import (
    DatabaseEnum, DatabaseUrlEnum, ErrorMessagesEnum,
    VariablePatternEnum, NormalizedParameterPrefix, VariableFormatEnum,
    EsKeysOfVariableMapping
)
from DataAccessLib.common.exceptions import InvalidSQLDataBase


__all__ = ["get_database", "get_database_url", "add_log", "SingletonDecorator", 'requests_retry_session',
           'remove_none_from_list', 'generate_parameter_pattern_from_normalized_variable', 'get_variable_value_key_based_on_format',
           'generate_parameter_pattern_from_normalized_variable_v2', 'change_date_format', 'get_variable_info']


def get_database(database):
    if database:
        if database not in [database.value for database in DatabaseEnum]:
            raise InvalidSQLDataBase(ErrorMessagesEnum.INVALID_SQL_DATABASE.value)
        return database
    return DatabaseEnum.MYSQL.value


def get_database_url(database):
    return {
        DatabaseEnum.MYSQL.value: DatabaseUrlEnum.MYSQL.value
    }.get(database)


def add_log(logger, value):
    if logger:
        logger.debug(value)


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


def requests_retry_session(retries=3, backoff_factor=0.5, status_forcelist=(500, 502, 504), session=None):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def remove_none_from_list(value):
    return list(filter(lambda v: v is not None, value))


def generate_parameter_pattern_from_normalized_variable(variable):
    """
        This function is generate parameter pattern from Normalized variable
        :param variable: STRING: Normalized value of variable from es
        visitor_phone_ok ---> ¿·$user.info.phone_ok·?
    """
    if variable.startswith(NormalizedParameterPrefix.CONTACT.value):
        return VariablePatternEnum.CONTACT.value.format(variable.replace(NormalizedParameterPrefix.CONTACT.value, ''))
    if variable.startswith(NormalizedParameterPrefix.CONVERSATION.value):
        return VariablePatternEnum.CONVERSATION.value.format(variable.replace(NormalizedParameterPrefix.CONVERSATION.value, ''))
    return variable


def get_variable_value_key_based_on_format(variable_format):
    """
        This method is use to decide key (value, value_date, value_double, value_boolean) of variable mapping in Es
        :param variable_format: STRING: variable format
    """
    return {
        **{}.fromkeys((VariableFormatEnum.TEXT.value, VariableFormatEnum.NAME.value,
                       VariableFormatEnum.EMAIL.value, VariableFormatEnum.PHONE.value), EsKeysOfVariableMapping.VALUE.value),
        VariableFormatEnum.DATE.value: EsKeysOfVariableMapping.VALUE_DATE.value,
        VariableFormatEnum.NUMBER.value: EsKeysOfVariableMapping.VALUE_DOUBLE.value,
        VariableFormatEnum.BOOLEAN.value: EsKeysOfVariableMapping.VALUE_BOOLEAN.value
    }.get(variable_format)

def generate_parameter_pattern_from_normalized_variable_v2(variables, normalized_variable):
    """
       This function is generate parameter pattern from Normalized variable
        :param variables: DICT: variables from redis
        :param normalized_variable: STRING: Normalized value of variable from es
        visitor_phone_ok ---> ¿·$user.info.phone_ok·?
    """
    return {
        'pattern': key for key, value in variables.items() if normalized_variable == value['normalized_parameter']
    }.get('pattern')


def change_date_format(_date: str):
    return datetime.fromisoformat(_date).strftime('%d-%b-%Y %I:%M %p')

def get_variable_info(variables, normalized_variable):
    if normalized_variable == "conversation_created_at":
        return {
            'type': VariableFormatEnum.DATE.value,
            'value_key': EsKeysOfVariableMapping.VALUE_DATE.value
        }
    variable = variables.get(generate_parameter_pattern_from_normalized_variable(normalized_variable), {})
    var_format = variable.get('format', VariableFormatEnum.TEXT.value)
    return {
        'type': var_format,
        'value_key': get_variable_value_key_based_on_format(var_format)
    }

