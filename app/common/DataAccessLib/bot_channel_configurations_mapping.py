from CachingLib import RedisOperationsTypeEnum
from UtilsLib import ChannelIdEnum
from DataAccessLib.common.enum import RedisKeyEnum
from DataAccessLib.common.utility import add_log, SingletonDecorator
from DataAccessLib.connection_network import ConnectionNetwork
from DataAccessLib.database.MySQL.bot_channel_configurations_mapping import (get_messenger_channel_bot_id,
                                                                             get_web_channel_bot_id,
                                                                             get_voiceweb_channel_bot_id,
                                                                             get_configured_bots)
from DataAccessLib.database.connect import SessionHandler
from DataAccessLib.handler import Getter, SyncDataHandler


@SingletonDecorator
class ManageBotChannelConfigurationMapping:
    """
    This class is used to manage the bot-channel configurations mapping. It has different type of Get methods to fetch
    the channel configurations related data.

    Bot-Channel configurations Get methods will follow below process.
        1. Get data from Cache
        2. If data not found then Invoke ``sync_data`` method of class "SyncDataHandler" to fetch the data from SQL
        and set in Cache.
    """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_bot_channel_configuration_mapping(self, channel_configuration_key, channel_id):
        """
        This method is used to fetch bot - channel_configuration mapping.

        :param channel_configuration_key: STRING: Unique channel configuration key
        :param channel_id: INTEGER: channel id
        :return: Account data if data found in Cache or SQL database else empty response
        """

        key = RedisKeyEnum.CHANNEL_CONFIGURATIONS_BOT_MAPPING.value.format(
            channel_configuration_key=channel_configuration_key)
        data = GetBotChannelConfigurationMapping.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger,
                    "Fetching data from SQL database for account {channel_configuration_key}".format(
                        channel_configuration_key=channel_configuration_key))

            data = SyncDataHandler.sync_data(self.config.db_session, self.config.cache_conn,
                                             GetBotChannelConfigurationMapping, key, channel_id=channel_id,
                                             channel_configuration_key=channel_configuration_key,
                                             logger=self.config.logger)
        return data


class GetBotChannelConfigurationMapping(Getter):
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

        return cache_conn.get(operation_type=RedisOperationsTypeEnum.GET.value,
                              payload={"key": key})

    @staticmethod
    def get_voiceweb_channel_bot_id(db_conn, logger, webhook_key):
        """
        This method is used to fetch data from the SQL voiceweb_channel_configurations table.

        Required parameters:
            :param db_conn: <<Class object>>
            :param logger: <<Class object>>
            :param webhook_key: Unique channel configurations key

        :return: Data if found else None
        """

        result = get_voiceweb_channel_bot_id(conn=db_conn, webhook_key=webhook_key)
        if result:
            return dict(bot_id=result.bot_id)
        add_log(logger,
                "No data for channel_configuration_key {webhook_key} in SQL database".format(webhook_key=webhook_key))

    @staticmethod
    def get_messenger_channel_bot_id(db_conn, logger, page_id):
        """
            This method is used to fetch data from the SQL facebook_pages & channel_configurations table.

        Required parameters:
            :param db_conn: <<Class object>>
            :param logger: <<Class object>>
            :param page_id: Unique page id

        :return: Data if found else None
        """

        result = get_messenger_channel_bot_id(conn=db_conn, page_id=page_id)
        if result:
            return dict(bot_id=result.bot_id)
        add_log(logger,
                "No data for channel_configuration_key {page_id} in SQL database".format(page_id=page_id))

    @staticmethod
    def get_web_channel_bot_id(db_conn, logger, publish_key):
        """
            This method is used to fetch data from the SQL bot_lead table.

        Required parameters:
            :param db_conn: <<Class object>>
            :param logger: <<Class object>>
            :param publish_key: Unique channel configurations key

        :return: Data if found else None
        """

        result = get_web_channel_bot_id(conn=db_conn, publish_key=publish_key)
        if result:
            return dict(bot_id=result.bot_id)
        add_log(logger,
                "No data for channel_configuration_key {publish_key} in SQL database".format(publish_key=publish_key))

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
        bot_id = None
        func = {
            ChannelIdEnum.FACEBOOK_MESSENGER.value: GetBotChannelConfigurationMapping.get_messenger_channel_bot_id,
            ChannelIdEnum.WEB.value: GetBotChannelConfigurationMapping.get_web_channel_bot_id,
            ChannelIdEnum.VOICEWEB.value: GetBotChannelConfigurationMapping.get_voiceweb_channel_bot_id
        }.get(kwargs['channel_id'])
        if func:
            with SessionHandler(db_session) as db_conn:
                bot_id = func(db_conn, logger, kwargs['channel_configuration_key'])
        return bot_id

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

        return str(data.get("bot_id")) if data.get("bot_id") else ''


@SingletonDecorator
class ManageBotsChannelConfigurationMapping:
    """
    This class is used to manage the bots-channel configurations mapping. It has different type of Get methods to fetch
    the channel configurations related data.
    Bot-Channel configurations Get methods will follow below process.
        1. Get data from Cache
        2. If data not found then Invoke ``sync_data`` method of class "SyncDataHandler" to fetch the data from SQL
        and set in Cache.
    """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_bots_channel_configuration_mapping(self, channel_configuration_key):
        """
        This method is used to fetch bots - channel_configuration mapping.
        :param channel_configuration_key: STRING: Unique channel configuration key
        :return: Bot list if data found in Cache or SQL database else empty response
        """

        key = RedisKeyEnum.BOTS_CHANNEL_CONFIGURATIONS_MAPPING.value.format(
            channel_configuration_key=channel_configuration_key)
        data = GetBotsChannelConfigurationMapping.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger,
                    "Fetching data from SQL database for account {channel_configuration_key}".format(
                        channel_configuration_key=channel_configuration_key))

            data = SyncDataHandler.sync_data(self.config.db_session, self.config.cache_conn,
                                             GetBotsChannelConfigurationMapping, key,
                                             channel_configuration_key=channel_configuration_key,
                                             logger=self.config.logger)
        return data


class GetBotsChannelConfigurationMapping(Getter):
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
        with SessionHandler(db_session) as db_conn:
            bots = get_configured_bots(db_conn, kwargs['channel_configuration_key'])
        return dict(bots=bots, channel_configuration_key=kwargs['channel_configuration_key'])

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

        return {
            "channel_configuration_key": data['channel_configuration_key'],
            "bots": [str(bot.bot_id) for bot in data['bots']],
            "account_id": str(data['bots'][0].account_id) if data['bots'] else None,
            "config_identity":  str(data['bots'][0].config_identity) if data['bots'] else None,
        }
