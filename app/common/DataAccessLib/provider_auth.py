from DataAccessLib.handler import Getter, SyncDataHandler
from CachingLib import RedisOperationsTypeEnum
from DataAccessLib.common.utility import SingletonDecorator, add_log
from DataAccessLib.connection_network import ConnectionNetwork
from DataAccessLib.database.connect import SessionHandler
from DataAccessLib.database.MySQL.provider_auth import get_twilio_managed_auth


@SingletonDecorator
class ManageProviderAuthDetails:
    """ This class is used to manage the Provider auth details """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_provider_auth_details(self, key, provider_name):
        """ This method is used to get Provider auth details """

        auth = GetProviderManagedAuth().get_data_from_cache(cache_conn=self.config.cache_conn, key=key)

        if not auth:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger, "Fetching data from SQL database for key `{key}`".format(key=key))

            auth = SyncDataHandler.sync_data(self.config.db_session,
                                             self.config.cache_conn,
                                             GetProviderManagedAuth,
                                             key,
                                             provider_name=provider_name,
                                             logger=self.config.logger)

        return auth or {}


class GetProviderManagedAuth(Getter):
    @staticmethod
    def get_data_from_cache(cache_conn, key, **kwargs):
        """
        It's overriding base class method ``get_data_from_cache`` and fetch bot data from the Cache database.
        It's using ``GetData`` class of ``caching`` package to perform this operation.
        """

        conversation = cache_conn.get(operation_type=RedisOperationsTypeEnum.GET_JSON.value, payload={"key": key})

        return conversation

    @staticmethod
    def get_data_from_sql(db_session, logger=None, **kwargs):
        """ Get conversations count from the MySQL """

        with SessionHandler(db_session) as db_conn:
            result = get_twilio_managed_auth(db_conn, kwargs.get('provider_name'))
        return result

    @staticmethod
    def prepare_sync_payload(data, es_result, **kwargs):
        """
        It will prepare payload to add data in Cache storage.

        Required parameters:
            :param data: <<Class object>>: Data fetched from the SQL
            :param es_result: <<Object>>: Data fetched from the elasticsearch

        Optional parameters:
            :param kwargs: Any extra arguments

        :return: Object
        """
        return data.auth
