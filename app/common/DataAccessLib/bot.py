from CachingLib import RedisOperationsTypeEnum
from UtilsLib import ChannelIdEnum
from DataAccessLib.common.enum import RedisKeyEnum
from DataAccessLib.common.utility import add_log, SingletonDecorator
from DataAccessLib.connection_network import ConnectionNetwork
from DataAccessLib.database.MySQL.bot import (get_bot_details,
                                              get_messenger_channel_configurations,
                                              get_bot_conversation_dialog,
                                              get_multiple_bot_trigger_rules,
                                              get_bot_version_from_sql, fetch_bot_id_by_publish_key)
from DataAccessLib.database.connect import SessionHandler
from DataAccessLib.handler import Getter, SyncDataHandler


@SingletonDecorator
class ManageBot:
    """
    This class is used to manage the bot operations. It has different type of Get methods to fetch the bot related
    data.

    Bot Get methods will follow below process.
        1. Get data from Cache
        2. If data not found then Invoke ``sync_data`` method of class "SyncDataHandler" to fetch the data from SQL
        and set in Cache.
    """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_bot_details(self, bot_id):
        """
        This method is used to fetch bot details.

        :param bot_id: INTEGER: Unique bot id
        :return: Bot data if data found in Cache or SQL database else empty response
        """

        key = RedisKeyEnum.BOT_DATA.value.format(bot_id=bot_id)
        data = GetBotDetails.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger, "Fetching data from SQL database for bot {bot_id}".format(bot_id=bot_id))

            data = SyncDataHandler.sync_data(
                self.config.db_session, self.config.cache_conn,
                GetBotDetails, key, bot_id=bot_id, logger=self.config.logger
            )
        return data

    def get_bot_flow_details(self, version_id):
        """
        This method is used to fetch bot flow.

        :param version_id: INTEGER: Unique version id
        :return: Bot Flow data if data found in Cache or SQL database else empty response
        """
        key = RedisKeyEnum.BOT_FLOW.value.format(version_id=version_id)
        data = GetBotFlowDetails.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger, "Fetching data from SQL database for version {version_id}".format(
                version_id=version_id))

            data = SyncDataHandler.sync_data(
                self.config.db_session, self.config.cache_conn,
                GetBotFlowDetails, key, version_id=version_id, logger=self.config.logger
            )
        return data

    def get_multiple_bot_trigger_rules(self, bot_ids):
        """
        This method is used to fetch bot trigger rules.

        :param bot_ids: LIST<INTEGER>: Unique bot id list
        :return: Bot trigger rules
        """
        keys = [RedisKeyEnum.BOT_TRIGGER_RULES.value.format(bot_id=bot_id) for bot_id in bot_ids]
        redis_trigger_rules = GetMultipleBotTriggerRules.get_data_from_cache(cache_conn=self.config.cache_conn,
                                                                             keys=keys)
        bot_trigger_rules = dict(zip(list(map(str, bot_ids)), redis_trigger_rules))
        missing_trigger_rules_bot_ids = GetMultipleBotTriggerRules.get_missing_trigger_rules_bot_ids(
            redis_trigger_rules,
            bot_ids)

        missing_bot_trigger_rules = GetMultipleBotTriggerRules.handle_missing_bot_trigger_rules(
            missing_trigger_rules_bot_ids,
            self.config.db_session,
            self.config.cache_conn)
        bot_trigger_rules.update(missing_bot_trigger_rules)
        return bot_trigger_rules

    def get_bot_versions(self, bot_id):
        return GetBotVersions.get_bot_versions(db_session=self.config.db_session, bot_id=bot_id)


class GetBotDetails(Getter):
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
    def get_channel_configurations(db_conn, channel_id, bot_id):
        """
        This method is used to get the cel configurations .
        Required parameters:
            :param db_conn: list <<Class object>>
            :param channel_id: INTEGER: channel id
            :param bot_id: INTEGER: id
        :return: DICT: channel configurations
        """
        channel_configurations = {}
        func = {
            ChannelIdEnum.FACEBOOK_MESSENGER.value: get_messenger_channel_configurations
        }.get(channel_id)
        if func and func(db_conn, bot_id):
            channel_configurations = func(db_conn, bot_id)._asdict()
        return channel_configurations

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
            bot_data = get_bot_details(conn=db_conn, bot_id=kwargs.get("bot_id"))
            if bot_data:
                channel_configurations = GetBotDetails.get_channel_configurations(db_conn, bot_data.channel_id, kwargs.get("bot_id"))
        if bot_data:
            return dict(bot_data=bot_data,
                        channel_configurations=channel_configurations)
        add_log(logger, "No data for bot {bot_id} in SQL database".format(bot_id=kwargs.get("bot_id")))

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

        bot_data = data.get("bot_data")
        user_first_name = bot_data.user_first_name if bot_data.user_first_name else ''
        user_last_name = bot_data.user_last_name if bot_data.user_last_name else ''
        return dict(bot_lead_id=bot_data.bot_id, preview_key=bot_data.preview_key, publish_key=bot_data.publish_key,
                    account_key=bot_data.account_key, account_id=bot_data.account_id,
                    latest_publish_version_id=bot_data.version_id,
                    latest_preview_version_id=bot_data.preview_version_id,
                    is_active=bot_data.is_active,
                    is_deleted=bot_data.is_deleted,
                    language=bot_data.language,
                    channel_id=bot_data.channel_id,
                    response_spreadsheet_id=bot_data.response_spreadsheet_id,
                    bot_title=bot_data.bot_title,
                    type=bot_data.type,
                    outbound_type=bot_data.outbound_type,
                    channel_configuration_id=bot_data.channel_configuration_id,
                    created_by=bot_data.created_by,
                    created_by_name='{} {}'.format(user_first_name, user_last_name),
                    created_at=str(bot_data.created_at),
                    sheet_id=bot_data.sheet_id,
                    spreadsheet_id=bot_data.spreadsheet_id,
                    trigger_variables=bot_data.trigger_variables,
                    channel_configurations=data.get("channel_configurations"),
                    campaign_details=bot_data.campaign_details)


class GetBotFlowDetails(Getter):
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
            conversation_dialog = get_bot_conversation_dialog(conn=db_conn, version_id=kwargs.get('version_id'))
        if conversation_dialog:
            return conversation_dialog
        add_log(logger, "No data found for conversation dialog {version_id} in SQL database".format(
            version_id=kwargs.get("version_id")))

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

        return data.conversation_dialog


class GetMultipleBotTriggerRules:
    @staticmethod
    def get_data_from_cache(cache_conn, keys, **kwargs):
        """
        This method is used to fetch data from the Cache database.

        Required parameters:
            :param cache_conn: <<Class object>>
            :param keys: STRING

        Optional parameters: It can be pass as a kwargs.

        :return Data if data found else None
        """

        return cache_conn.get(operation_type=RedisOperationsTypeEnum.GET_MULTIPLE.value,
                              payload={"keys": keys})

    @staticmethod
    def get_missing_trigger_rules_bot_ids(data, bot_ids):
        """This method is used to get the missing trigger rules bot ids which is not presents in the cache"""

        return [bot_ids[index] for index in range(len(data)) if not data[index]]

    @staticmethod
    def get_data_from_sql(db_session, bot_ids):
        """
        This method is used to fetch data from the SQL database.

        Required parameters:
            :param db_session: <<Class object>>
            :param bot_ids: List


        :return: Data if found else empty list
        """
        with SessionHandler(db_session) as db_conn:
            bot_trigger_rules = get_multiple_bot_trigger_rules(conn=db_conn, bot_ids=bot_ids)
        if bot_trigger_rules:
            return bot_trigger_rules
        return []

    @staticmethod
    def prepare_sync_payload(trigger_rules):
        """
        It will prepare payload to add data in Cache storage.

        Required parameters:
            :param trigger_rules: bot trigger rules

        :return: Object
        """

        return trigger_rules

    @staticmethod
    def set_data_in_cache(cache_conn, key, value, path="."):

        cache_conn.set(operation_type=RedisOperationsTypeEnum.SET_JSON.value,
                       payload={"key": key, "value": value, "path": path})

    @staticmethod
    def handle_missing_bot_trigger_rules(bot_ids, db_session, cache_conn):
        """This method is used to handle the missing bot trigger rules
        - Get data from sql
        - Prepare payload
        - Sync Data into the Redis

        :return: Missing  bot trigger rules
        """

        missing_bot_trigger_rules = {}

        if bot_ids:
            mysql_data = GetMultipleBotTriggerRules.get_data_from_sql(db_session, bot_ids)
            for bot_trigger_rules_data in mysql_data:
                bot_id = bot_trigger_rules_data.bot_id
                trigger_rules = bot_trigger_rules_data.trigger_rules
                if trigger_rules:
                    sync_payload = GetMultipleBotTriggerRules.prepare_sync_payload(trigger_rules)
                    key = RedisKeyEnum.BOT_TRIGGER_RULES.value.format(bot_id=bot_id)
                    GetMultipleBotTriggerRules.set_data_in_cache(cache_conn, key, sync_payload)
                    missing_bot_trigger_rules[str(bot_id)] = sync_payload
        return missing_bot_trigger_rules


class GetBotVersions:

    @staticmethod
    def get_bot_versions(db_session, bot_id):
        """Get bot version by bot id"""

        with SessionHandler(db_session) as db_conn:
            bot_versions = get_bot_version_from_sql(db_conn, bot_id)
        return [bot_version.version_id for bot_version in bot_versions]


class GetBotLeadId:
    def __init__(self):
        self.config = ConnectionNetwork()

    def get_bot_id_by_publish_key(self, publish_key):
        key = RedisKeyEnum.BOT_PUBLISH_KEY_ID_MAPPING.value.format(publish_key=publish_key)
        data = GetBotLeadId.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)

        if data:
            return int(data)
        else:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger, "Fetching data from SQL database for publish_key {publish_key}".format(publish_key=publish_key))

            data = SyncDataHandler.sync_data(
                self.config.db_session, self.config.cache_conn,
                GetBotLeadId, key, publish_key=publish_key, logger=self.config.logger
            )
            return data

    @staticmethod
    def get_data_from_cache(cache_conn, key):
        """
        This method is used to fetch data from the Cache database.

        Required parameters:
            :param cache_conn: <<Class object>>
            :param key: STRING

        :return Data if data found else None
        """
        return cache_conn.get(
            operation_type=RedisOperationsTypeEnum.GET.value,
            payload={"key": key}
        )

    @staticmethod
    def get_data_from_sql(db_session, logger=None, **kwargs):
        """
        This method is used to fetch data from the SQL database.

        Required parameters:
            :param db_session: <<Class object>>

        Optional Parameters:
            :param logger: <<Class object>>
            :param kwargs: Extra arguments


        :return: Data if found else None
        """

        with SessionHandler(db_session) as db_conn:
            bot_lead_id = fetch_bot_id_by_publish_key(conn=db_conn, publish_key=kwargs.get("publish_key"))

        if bot_lead_id:
            return bot_lead_id

        add_log(logger, "No data found for publish key {publish_key} in SQL database".format(
            publish_key=kwargs.get("publish_key")))

    @staticmethod
    def prepare_sync_payload(bot_lead_id, es_result, **kwargs):
        """
        It will prepare payload to add data in Cache storage.

        Required parameters:
            :param bot_lead_id: bot id
            :param es_result: <<Object>>: Data fetched from the elasticsearch

        :return: Object
        """
        return bot_lead_id

    @staticmethod
    def get_data_from_elasticsearch(logger=None, **kwargs):
        """
        Its overriding base class method ``get_data_from_elasticsearch``.
        Here we don't require to fetch anything from the elastic search. So it will return an empty object
        """
        return {}
