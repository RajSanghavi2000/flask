from CachingLib import RedisOperationsTypeEnum
from UtilsLib import ChannelIdEnum
from DataAccessLib.common.enum import RedisKeyEnum
from DataAccessLib.common.utility import add_log, SingletonDecorator
from DataAccessLib.connection_network import ConnectionNetwork
from DataAccessLib.database.MySQL.channel_configuration import (get_channel_configuration)
from DataAccessLib.database.connect import SessionHandler
from DataAccessLib.handler import Getter, SyncDataHandler


@SingletonDecorator
class ManageChannelConfiguration:
    """
    This class is used to manage the channel configurations. It has different type of Get methods to fetch
    the channel configurations related data.

    Channel configurations Get methods will follow below process.
        1. Get data from Cache
        2. If data not found then Invoke ``sync_data`` method of class "SyncDataHandler" to fetch the data from SQL
        and set in Cache.
    """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_channel_configuration(self, channel_configuration_id):
        """
        This method is used to fetch channel configuration.

        :param channel_configuration_id: INTEGER: Channel configuration id
        :return: Account data if data found in Cache or SQL database else empty response
        """

        key = RedisKeyEnum.CHANNEL_CONFIGURATION.value.format(
            channel_configuration_id=channel_configuration_id
        )
        data = GetChannelConfiguration.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger,
                    "Fetching data from SQL database for channel-configuration-id: {channel_configuration_id}".format(
                        channel_configuration_id=channel_configuration_id))

            data = SyncDataHandler.sync_data(self.config.db_session, self.config.cache_conn,
                                             GetChannelConfiguration, key,
                                             channel_configuration_id=channel_configuration_id,
                                             logger=self.config.logger)
        return data


class GetChannelConfiguration(Getter):
    @staticmethod
    def get_data_from_cache(cache_conn, key, **kwargs):
        """
        This method is used to fetch data from the Cache database.

        Required parameters:
            :param cache_conn: <<Class object>>
            :param key: STRING

        Optional parameters: It can be pass as a kwargs.

        :return Data if data found else None
        """

        return cache_conn.get(operation_type=RedisOperationsTypeEnum.GET_JSON.value,
                              payload={"key": key})

    @staticmethod
    def get_data_from_sql(db_session, logger=None, **kwargs):
        """
        This method is used to fetch data from the SQL database.

        Required parameters:
            :param db_session: <<Class object>>

        Optional Parameters:
            :param logger: <<Class object>>
            :param kwargs: Extra arguments

        :return: Data if found else empty object {}
        """
        """
        This method is used to get the channel configurations .
        Required parameters:
            :param db_conn: list <<Class object>>
            :param bot_id: INTEGER: id
        :return: DICT: channel configuration
        """
        channel_configurations = {}
        with SessionHandler(db_session) as db_conn:
            db_channel_configurations = get_channel_configuration(
                conn=db_conn,
                channel_configuration_id=kwargs.get('channel_configuration_id')
            )
        if db_channel_configurations:
            channel_configurations = db_channel_configurations._asdict()
        else:
            add_log(logger, "No data for channel-configuration-id {channel_configuration_id} in SQL database".format(
                channel_configuration_id=kwargs.get("channel_configuration_id")
            ))
        return dict(channel_configurations=channel_configurations)


    @staticmethod
    def get_data_from_elasticsearch(logger=None, **kwargs):
        """
        Its overriding base class method ``get_data_from_elasticsearch``. Here we don't require to fetch anything from
        the elastic search so it will return empty object
        """
        return {}

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

        return data.get("channel_configurations", {})