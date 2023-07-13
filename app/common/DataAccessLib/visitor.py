import math
import os

from DataAccessLib.handler import Getter, SyncDataHandler
from CachingLib import RedisOperationsTypeEnum
from DataAccessLib.common.enum import (RedisKeyEnum, VisitorActiveConversationKeyEnum, VisitorVariablesNameEnum,
                                       IgnoreVisitorVariablesEnum, VariablesTypeEnum, SystemVariablesEnum,
                                       SystemVariablesParameterEnum)
from DataAccessLib.database.MySQL.visitor import (get_visitor_from_sql, get_visitor_key_using_external_key,
                                                  get_visitor_default_name_counter_and_series)
from DataAccessLib.common.utility import (
    add_log, SingletonDecorator, EsKeysOfVariableMapping,
    change_date_format, get_variable_info
)
from DataAccessLib.database.connect import SessionHandler
from DataAccessLib.connection_network import ConnectionNetwork
from DataAccessLib.database.elasticsearch.visitor import get_visitor_variables_from_es_variables
from DataAccessLib.common.constants import VISITOR_NAME_SERIES, VISITOR_NAME_PATTERN
from DataAccessLib.database.elasticsearch.visitor import get_conversation_data_from_summary_index
from DataAccessLib.variable import ManageVariable


@SingletonDecorator
class ManageVisitor:
    """
    This class is used to manage the visitor operations.

    Visitor Get methods will follow below process.
        1. Get data from Cache
        2. If data not found then Invoke ``sync_data`` method of class "SyncDataHandler" to fetch the data from SQL
        and set in Cache.
    """

    def __init__(self):
        self.config = ConnectionNetwork()

    def redis_get_visitor_key(self, external_key):
        """
        This method is used to get visitor key from redis

        :param external_key: STRING: External system key to identify visitor uniquely across the channel
        """
        key = RedisKeyEnum.VISITOR_EXTERNAL_KEY.value.format(external_key=external_key)
        return GetVisitorKeyUsingExternalKey.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)

    def redis_get_visitor(self, visitor_key):
        """
        This method is used to get visitor from redis

        :param visitor_key: STRING: Unique key assigned to every visitor
        """

        key = RedisKeyEnum.VISITOR.value.format(visitor_key=visitor_key)
        visitor = GetVisitorByVisitorKey.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if visitor:
            self._format_visitor_schema(visitor_key, visitor)
            return visitor
        return {}

    def get_visitor(self, key='', external_key=''):
        """
        This method is sued to get visitor object

        :param key: STRING: Unique key assigned to every visitor
        :param external_key: STRING: External system key to identify visitor uniquely across the channel
        """

        visitor = {}
        if not key:
            key = self.__get_visitor_by_external_key(external_key)

        if key:
            visitor = self.__get_visitor_by_visitor_key(key)

        return visitor

    @staticmethod
    def _format_visitor_schema(visitor_key, visitor):
        visitor['key'] = visitor_key
        visitor['is_new'] = False
        for key, value in visitor['variables'].items():
            visitor['variables'][key]['type'] = VariablesTypeEnum.CONTACT.value

    def __get_visitor_by_visitor_key(self, visitor_key):
        """
        This method is used to get visitor object using visitor key

        :param key: STRING: Unique key assigned to every visitor
        """
        key = RedisKeyEnum.VISITOR.value.format(visitor_key=visitor_key)
        visitor = GetVisitorByVisitorKey.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not visitor:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger, "Fetching data from SQL database for key {key}".format(key=key))

            visitor = SyncDataHandler.sync_data(self.config.db_session, self.config.cache_conn,
                                                GetVisitorByVisitorKey, key=key,
                                                logger=self.config.logger, visitor_key=visitor_key,
                                                redis_key_expire_time=os.environ.get("REDIS_VISITOR_KEY_EXPIRATION_TIME", 604800))

        if visitor:
            self._format_visitor_schema(visitor_key, visitor)

        return visitor

    def __get_visitor_by_external_key(self, external_key):
        """
        This method is sued to get visitor object using external key

        :param external_key: STRING: External system key to identify visitor uniquely across the channel
        """

        key = RedisKeyEnum.VISITOR_EXTERNAL_KEY.value.format(external_key=external_key)
        data = GetVisitorKeyUsingExternalKey.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger,
                    "Fetching data from SQL database for key {key}".format(key=key))

            return SyncDataHandler.sync_data(self.config.db_session, self.config.cache_conn,
                                             GetVisitorKeyUsingExternalKey, key=key,
                                             logger=self.config.logger, external_key=external_key)
        return data


class GetVisitorByVisitorKey(Getter):
    @staticmethod
    def get_data_from_cache(cache_conn, key, **kwargs):
        """
        It's overriding base class method ``get_data_from_cache`` and fetch bot data from the Cache database. It's using ``GetData``
        class of ``caching`` package to perform this operation.
        """

        visitor = cache_conn.get(operation_type=RedisOperationsTypeEnum.GET_JSON.value, payload={"key": key})

        return visitor

    @staticmethod
    def get_data_from_sql(db_session, logger=None, **kwargs):
        """
        Its overriding base class method ``get_data_from_sql`` and fetch bot data from the SQL database. It's using
        ``SQLAlchemy`` to get the data.
        """

        with SessionHandler(db_session) as db_conn:
            visitor = get_visitor_from_sql(db_conn, kwargs.get('visitor_key'))

            if visitor:
                return dict(visitor=visitor)

    @staticmethod
    def get_data_from_elasticsearch(logger=None, **kwargs):
        """
        Its overriding base class method ``get_data_from_elasticsearch``. Here we don't require to fetch anything from
        the elastic search so it will return empty object
        """

        if kwargs.get('db_data'):
            return {'variables': get_visitor_variables_from_es_variables(kwargs.get('db_data')['visitor'][0].key),
                    'conversations_data': get_conversation_data_from_summary_index(
                        kwargs.get('db_data')['visitor'][0].key)}

    @staticmethod
    def prepare_sync_payload(data, es_result, **kwargs):
        """
        It's overriding base class method ``prepare_sync_payload`` and prepare bot payload to store data into the
        Cache storage
        """

        variables = GetVisitorByVisitorKey.filter_visitor_variables_from_es_result(es_result.get('variables'))

        visitor_payload = {"variables": variables, "active_conversations": {}}

        if data['visitor']:
            visitor_payload['id'] = data['visitor'][0].id
            visitor_payload['external_key'] = data['visitor'][0].external_key
            visitor_payload['account_id'] = data['visitor'][0].account_id
            visitor_payload['channel_id'] = data['visitor'][0].channel_id

        for conversation in es_result.get('conversations_data'):
            visitor_payload['active_conversations'][VisitorActiveConversationKeyEnum.SUFFIX.value.format(
                conversation_external_key=conversation.get("_source", {}).get('conversation_external_key'),
                bot_id=conversation.get("_source", {}).get('bot_id'))] = conversation.get("_source", {}).get(
                'thread_key')

            visitor_payload['default_name'] = conversation.get("_source", {}).get('conversation_title')

        if not visitor_payload.get('default_name'):
            visitor_payload['default_name'] = VisitorDefaultName.get_default_name(
                visitor_payload.get('account_id'),
                kwargs.get("cache_conn"),
                kwargs.get("db_session")
            )

        return visitor_payload


    @staticmethod
    def filter_visitor_variables_from_es_result(es_result):
        """This method is used to separate visitor variables from the elasticsearch result"""

        variables = {}
        payload = es_result.get('_source', {})
        account_variables = GetVisitorByVisitorKey.get_account_variables(payload.get("account_id"))

        for item in payload.get("variables", []):
            if item.get("name").startswith(VisitorVariablesNameEnum.VISITOR_ES_PREFIX.value) and item.get(
                    "name") not in IgnoreVisitorVariablesEnum.VARIABLES.value:
                variables[VisitorVariablesNameEnum.PREFIX.value.format(variable=item.get("name").replace(
                    VisitorVariablesNameEnum.VISITOR_ES_PREFIX.value, ''
                ))] = {"value":  GetVisitorByVisitorKey.get_value(account_variables, item)}
            if item.get("name") == SystemVariablesEnum.CONTACT_ID.value:
                variables[SystemVariablesParameterEnum.CONTACT_ID.value] = \
                    {"value": GetVisitorByVisitorKey.get_value(account_variables, item)}
        return variables

    @staticmethod
    def get_value(account_variables, item):
        value_key = GetVisitorByVisitorKey.get_variable_value_key(account_variables, item.get("name"))
        return item.get(value_key)

    @staticmethod
    def get_account_variables(account_id):
        return ManageVariable().get_variables(account_id) or {}

    @staticmethod
    def get_variable_value_key(account_variables, variable_name):
        """
            In Es variables is Stored as normalized patten like (visitor_phone_ok)
            this method is generate patten like ¿·$user.info.phone_ok·? from this `visitor_phone_ok`
            and find format of variable based on return value key.
        """
        variable = get_variable_info(account_variables, variable_name)
        return variable.get('value_key')

    @staticmethod
    def generate_variable_pattern(variable_name):
        return generate_parameter_pattern_from_normalized_variable(variable_name)



class GetVisitorKeyUsingExternalKey(Getter):
    @staticmethod
    def get_data_from_cache(cache_conn, key, **kwargs):
        """
        It's overriding base class method ``get_data_from_cache`` and fetch bot data from the Cache database. It's using ``GetData``
        class of ``caching`` package to perform this operation.
        """

        return cache_conn.get(operation_type=RedisOperationsTypeEnum.GET.value, payload={"key": key})

    @staticmethod
    def get_data_from_sql(db_session, logger=None, **kwargs):
        """
        Its overriding base class method ``get_data_from_sql`` and fetch bot data from the SQL database. It's using
        ``SQLAlchemy`` to get the data.
        """

        with SessionHandler(db_session) as db_conn:
            result = get_visitor_key_using_external_key(db_conn, kwargs.get("external_key"))

            if result:
                return dict(visitor_key=result.visitor_key)

    @staticmethod
    def get_data_from_elasticsearch(logger=None, **kwargs):
        """
        Its overriding base class method ``get_data_from_elasticsearch``. Here we don't require to fetch anything from
        the elasticsearch so it will return empty object
        """
        pass

    @staticmethod
    def prepare_sync_payload(data, es_result, **kwargs):
        """
        It's overriding base class method ``prepare_sync_payload`` and prepare bot payload to store data into the
        Cache storage
        """

        return data['visitor_key']


class VisitorDefaultName:
    @staticmethod
    def get_default_name(account_id, cache_conn, db_session):
        """
        This method is used to generate visitor default name
        """
        max_visitor_count = int(os.environ.get('MAX_SERIES_NO_FOR_VISITOR_COUNT'))
        prefix = os.environ.get("VISITOR_NAME_PREFIX")

        counter, series = VisitorDefaultName.get_default_name_series_and_counter(account_id, max_visitor_count,
                                                                                 cache_conn, db_session)
        if counter > max_visitor_count:
            if series == VISITOR_NAME_SERIES[-1]:
                series = VISITOR_NAME_SERIES[0]
            else:
                series = VISITOR_NAME_SERIES[VISITOR_NAME_SERIES.index(series) + 1]

        return VISITOR_NAME_PATTERN.format(prefix=prefix, series=series, sequence=counter)

    @staticmethod
    def get_default_name_series_and_counter(account_id, max_counter, cache_conn, db_session):
        """
        Get default_name series and counter from the database based on the account id.
        - Get default_name series and Incremented counter form the Redis
        - If not found in Redis
        - Get data from the SQL
        - Add default_name series and counter into the Redis
        - Increment visitor counter in Redis

        :return:
            counter: Integer
            series: String
        """

        counter = VisitorDefaultName._get_visitor_counter_from_redis(cache_conn, account_id)
        if counter is None:
            with SessionHandler(db_session) as db_conn:
                result = get_visitor_default_name_counter_and_series(db_conn, account_id)
            payload = dict(counter=result.count)
            VisitorDefaultName._update_visitor_counter_in_redis(cache_conn, account_id, payload)
            counter = VisitorDefaultName._get_visitor_counter_from_redis(cache_conn, account_id)
        counter, series = VisitorDefaultName.get_visitor_pattern(count=counter, max_visitor_count=max_counter)
        return counter, series

    @staticmethod
    def get_visitor_pattern(count, max_visitor_count):
        """Get visitor counter and series based on the visitor counts and max_visitor_count"""
        if count:
            visitor_count = max_visitor_count if (count % max_visitor_count) == 0 else (count % max_visitor_count)
            visitor_name_series = VISITOR_NAME_SERIES[
                ((math.ceil(count / max_visitor_count)) % len(VISITOR_NAME_SERIES)) - 1]
            return visitor_count, visitor_name_series
        return 1, VISITOR_NAME_SERIES[0]

    @staticmethod
    def _get_visitor_counter_from_redis(cache_conn, account_id):
        """
        This method is used to get account's visitor counter from Redis. It will increment counter and then
        return the incremented counter. If key is present else it will return `None`

        :param account_id: Unique account ID
        """

        try:
            return cache_conn.update(
                operation_type=RedisOperationsTypeEnum.INCREMENT_VALUE.value,
                payload={
                    "key": RedisKeyEnum.VISITOR_DEFAULT_NAME.value.format(account_id=account_id),
                    "value": 1,
                    "path": 'counter'
                }
            )
        except Exception:
            pass

    @staticmethod
    def _update_visitor_counter_in_redis(cache_conn, account_id, payload):
        """
        This method is used to update visitor counter object into the Redis

        :param account_id: Unique id per account
        :param payload: Payload to add in Redis

        :return: None
        """
        cache_conn.set(operation_type=RedisOperationsTypeEnum.SET_JSON_NX.value, payload={
            "key": RedisKeyEnum.VISITOR_DEFAULT_NAME.value.format(account_id=account_id), "value": payload})
