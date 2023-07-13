import json

from CachingLib import RedisOperationsTypeEnum
from UtilsLib import decode_unicode_dict

from DataAccessLib.common.constants import BOT_TYPES, IN_PROGRESS, DELETED, RESOURCES
from DataAccessLib.common.enum import RedisKeyEnum
from DataAccessLib.common.utility import add_log, SingletonDecorator
from DataAccessLib.connection_network import ConnectionNetwork
from DataAccessLib.database.MySQL.account import (get_account_details,
                                                  get_bot_list,
                                                  get_account_features,
                                                  get_account_popup_messages,
                                                  get_outbound_messages_total_balance, get_account_bots,
                                                  get_multiple_account_bots,
                                                  get_account_delete_resource,
                                                  get_account_resource_stats,
                                                  get_account_total_visitor_count, fetch_account_id_by_account_key)
from DataAccessLib.database.elasticsearch.account import get_used_outbound_messages_balance
from DataAccessLib.database.connect import SessionHandler
from DataAccessLib.handler import Getter, SyncDataHandler
from UtilsLib import str_datetime, DT_FMT_Ymd


@SingletonDecorator
class ManageAccount:
    """
    This class is used to manage the account operations. It has different type of Get methods to fetch the account
    related data.

    Account Get methods will follow below process.
        1. Get data from Cache
        2. If data not found then Invoke ``sync_data`` method of class "SyncDataHandler" to fetch the data from SQL
        and set in Cache.
    """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_account_details(self, account_id):
        """
        This method is used to fetch account details.

        :param account_id: INTEGER: Unique account id
        :return: Account data if data found in Cache or SQL database else empty response
        """

        key = RedisKeyEnum.ACCOUNT_DATA.value.format(account_id=account_id)
        data = GetAccountDetails.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger,
                    "Fetching data from SQL database for account {account_id}".format(account_id=account_id))

            data = SyncDataHandler.sync_data(self.config.db_session, self.config.cache_conn,
                                             GetAccountDetails, key, account_id=account_id, logger=self.config.logger)
        return data

    def get_multiple_account_details(self, account_ids):
        """
        This method is used to fetch multiple account details.

        :param account_ids: LIST<INTEGER>: Unique account id list
        :return: Multiple account object
        """
        keys = [RedisKeyEnum.ACCOUNT_DATA.value.format(account_id=account_id) for account_id in account_ids]
        redis_account_details = GetMultipleAccountDetails.get_data_from_cache(cache_conn=self.config.cache_conn,
                                                                              keys=keys)
        redis_account_details = decode_unicode_dict(redis_account_details)
        account_details = dict(zip(list(map(str, account_ids)), redis_account_details))
        missing_account_ids = GetMultipleAccountDetails.get_missing_account_ids(
            redis_account_details,
            account_ids)
        missing_account_details = GetMultipleAccountDetails.handle_missing_account_details(
            missing_account_ids,
            self.config.db_session,
            self.config.cache_conn)
        account_details.update(missing_account_details)
        return account_details

    def get_outbound_messages_remaining_balance(self, account_id):
        """
        This method is used to fetch account details.

        :param account_id: INTEGER: Unique account id
        :return: Account data if data found in Cache or SQL database else empty response
        """

        key = RedisKeyEnum.OUTBOUND_REMAINING_BALANCE.value.format(account_id=account_id)
        data = GetOutboundMessagesRemainingBalance.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger,
                    "Fetching data from SQL database for account {account_id}".format(account_id=account_id))

            data = SyncDataHandler.sync_data(self.config.db_session, self.config.cache_conn,
                                             GetOutboundMessagesRemainingBalance, key, account_id=account_id, logger=self.config.logger)
        return data

    def get_account_bots(self, account_id, bot_type=BOT_TYPES):
        """ This method is used get account bots
        :param: account_id: Unique account ID
        :param: bot_type: Bot Type, Default is ('inbound', 'outbound')
        """

        return GetAccountDetails.get_account_bots(self.config.db_session, account_id, bot_type)

    def get_multiple_account_bots(self, account_ids, bot_type=BOT_TYPES):
        """ This method is used get multiple account bots

        :param: account_ids: LIST: Unique account IDs list
        :param: bot_type: Bot Type, Default is ('inbound', 'outbound')
        """

        return GetAccountDetails.get_multiple_account_bots(self.config.db_session, account_ids, bot_type)

    def get_account_total_visitor_count(self, account_id):
        """ This method is used to get account total conversation count """

        return GetAccountDetails().get_account_total_visitor_count(self.config.db_session, account_id)


class GetAccountDetails(Getter):
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
            account_data = get_account_details(conn=db_conn, account_ids=[kwargs.get("account_id")])
            bot_list = get_bot_list(conn=db_conn, account_ids=[kwargs.get("account_id")], include_deleted_bots=True)

            non_deleted_bots, deleted_bots = GetAccountDetails.get_deleted_non_deleted_bots(bot_list)
            popup_messages = get_account_popup_messages(conn=db_conn, account_ids=[kwargs.get("account_id")])

        if account_data:
            features = get_account_features(conn=db_conn, account_ids=[kwargs.get("account_id")])
            return dict(
                account_data=account_data[0],
                bots=non_deleted_bots,
                deleted_bots=deleted_bots,
                features=features,
                popup_messages=popup_messages
            )
        add_log(logger, "No data for account {account_id} in SQL database".format(account_id=kwargs.get("account_id")))

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

        account_data = data.get("account_data")
        features = data.get("features")
        bots = {"bots": data.get("bots"), "deleted_bots": data.get("deleted_bots", [])}
        popup_messages = data.get("popup_messages")
        features = {feature.key: GetAccountDetails.parse_features(feature) for feature in features}
        subscription = GetAccountDetails.get_subscription_object(account_data, features)
        popup_messages = [GetAccountDetails().parse_popup_message_data(popup_message)
                          for popup_message in popup_messages]
        return GetAccountDetails.parse_account_object(account_data, bots, subscription, popup_messages)

    @staticmethod
    def parse_account_object(account_data, bots, subscription, popup_messages):
        return dict(account_id=account_data.account_id,
                    account_name=account_data.account_name,
                    account_key=account_data.account_key,
                    owner_id=account_data.owner_id,
                    timezone=account_data.timezone,
                    image_name=account_data.image_name,
                    payment_method=account_data.payment_method,
                    account_status=account_data.account_status,
                    operating_hours=json.dumps(account_data.operating_hours) if account_data.operating_hours else None,
                    enabled_human_handover=account_data.enabled_human_handover,
                    maximum_chat_allocation_limit=account_data.maximum_chat_allocation_limit,
                    returning_user_cookie_duration=account_data.returning_user_cookie_duration,
                    feature_integration=account_data.feature_integration,
                    feature_configuration=account_data.feature_configuration,
                    outbound_configuration=account_data.outbound_configuration,
                    live_chat_configurations=account_data.live_chat_configurations,
                    is_domain_restricted=int(account_data.is_domain_restricted),
                    registered_domains=account_data.registered_domains
                    if account_data.registered_domains and json.loads(account_data.registered_domains) else None,
                    site_url=json.loads(account_data.site_url) if account_data.site_url else None,
                    bots=bots.get('bots'),
                    deleted_bots=bots.get('deleted_bots', []),
                    trigger_event=account_data.trigger_event,
                    is_unassign_conversation_on_auto_assignment_failure_enabled=
                    account_data.is_unassign_conversation_on_auto_assignment_failure_enabled,
                    subscription=subscription,
                    popup_messages=popup_messages)

    @staticmethod
    def parse_popup_message_data(popup_message):
        return {
            "id": popup_message.id,
            "url_regex": popup_message.url_regex,
            "message": popup_message.message
        }

    @staticmethod
    def get_subscription_object(account_data, features):
        return {
            "id": account_data.subscription_id,
            "activation_source": account_data.plan_source,
            "plan": {
                "id": account_data.plan_id,
                "name": account_data.plan_name
            },
            "features": features
        }

    @staticmethod
    def parse_features(feature):
        return {
            "id": feature.feature_id,
            "config": feature.config
        }

    @staticmethod
    def filter_deleted_non_deleted_bots(bot, deleted_bots, non_deleted_bots):
        if bot.is_deleted:
            deleted_bots.append(str(bot.id))
        else:
            non_deleted_bots.append(str(bot.id))

    @staticmethod
    def get_deleted_non_deleted_bots(bots):
        """ This method is used to get deleted & non deleted bots """
        deleted_bots = []
        non_deleted_bots = []
        for bot in bots:
            GetAccountDetails.filter_deleted_non_deleted_bots(bot, deleted_bots, non_deleted_bots)
        return non_deleted_bots, deleted_bots

    @staticmethod
    def get_account_bots(db_session, account_id, bot_type):
        """ This method is used to get account bots """

        with SessionHandler(db_session) as db_conn:
            bots = get_account_bots(conn=db_conn, account_id=account_id, bot_type=bot_type)
        bots = [bot.id for bot in bots]
        return bots

    @staticmethod
    def get_multiple_account_bots(db_session, account_ids, bot_type):
        """ This method is used to get multiple account bots """

        with SessionHandler(db_session) as db_conn:
            accounts_bots = get_multiple_account_bots(conn=db_conn, account_ids=account_ids, bot_type=bot_type)
        account_bots_mapping = {str(account_id): [] for account_id in account_ids}
        for bot in accounts_bots:
            account_id = str(bot.account_id)
            account_bots = account_bots_mapping.get(account_id, [])
            account_bots.append(str(bot.id))
            account_bots_mapping[account_id] = account_bots
        return account_bots_mapping

    @staticmethod
    def get_account_total_visitor_count(db_session, account_id):
        with SessionHandler(db_session) as db_conn:
            visitors = get_account_total_visitor_count(conn=db_conn, account_id=account_id)
        return visitors.count


class GetMultipleAccountDetails:
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
    def get_missing_account_ids(data, account_ids):
        """This method is used to get the missing account ids which is not presents in the cache"""

        return [account_ids[index] for index in range(len(data)) if not data[index]]

    @staticmethod
    def get_empty_bot_list():
        return {"bots": [], "deleted_bots": []}

    @staticmethod
    def parse_sql_account_bots(bot_list):
        account_bots = {}
        for bot in bot_list:
            account_id = str(bot.account_id)
            bot_ids = account_bots.get(account_id, GetMultipleAccountDetails.get_empty_bot_list())
            deleted_bots = bot_ids['deleted_bots']
            non_deleted_bots = bot_ids['bots']
            GetAccountDetails.filter_deleted_non_deleted_bots(bot, deleted_bots, non_deleted_bots)
            account_bots[account_id] = {"bots": non_deleted_bots, "deleted_bots": deleted_bots}
        return account_bots

    @staticmethod
    def parse_sql_account_popup_messages(popup_message_list):
        account_popup_messages = {}
        for popup_message in popup_message_list:
            account_id = str(popup_message.account_id)
            popup_messages = account_popup_messages.get(account_id, [])
            popup_messages.append(GetAccountDetails.parse_popup_message_data(popup_message))
            account_popup_messages[account_id] = popup_messages
        return account_popup_messages

    @staticmethod
    def parse_sql_account_features(feature_list):
        account_features = {}
        for feature in feature_list:
            account_id = str(feature.account_id)
            features = account_features.get(account_id, {})
            features[feature.key] = GetAccountDetails.parse_features(feature)
            account_features[account_id] = features
        return account_features

    @staticmethod
    def get_data_from_sql(db_session, account_ids):
        """
        This method is used to fetch data from the SQL database.

        Required parameters:
            :param db_session: <<Class object>>
            :param account_ids: List


        :return: Data if found else empty list
        """
        sync_payload_list = []
        with SessionHandler(db_session) as db_conn:
            account_details = get_account_details(conn=db_conn, account_ids=account_ids)
            bot_list = get_bot_list(conn=db_conn, account_ids=account_ids, include_deleted_bots=True)
            popup_message_list = get_account_popup_messages(conn=db_conn, account_ids=account_ids)
            feature_list = get_account_features(conn=db_conn, account_ids=account_ids)

        account_bots = GetMultipleAccountDetails.parse_sql_account_bots(bot_list)
        account_popup_messages = GetMultipleAccountDetails.parse_sql_account_popup_messages(popup_message_list)
        account_features = GetMultipleAccountDetails.parse_sql_account_features(feature_list)

        for account_detail in account_details:
            account_id = str(account_detail.account_id)
            bots = account_bots.get(account_id, GetMultipleAccountDetails.get_empty_bot_list())
            popup_messages = account_popup_messages.get(account_id, [])
            features = account_features.get(account_id, {})
            subscription = GetAccountDetails.get_subscription_object(account_detail, features)
            sync_payload_list.append(GetMultipleAccountDetails.prepare_sync_payload(account_detail, bots, subscription,
                                                                                    popup_messages))
        return sync_payload_list

    @staticmethod
    def prepare_sync_payload(account_data, bots, subscription, popup_messages):
        return GetAccountDetails.parse_account_object(account_data, bots, subscription, popup_messages)

    @staticmethod
    def set_data_in_cache(cache_conn, key, value, path="."):

        cache_conn.set(operation_type=RedisOperationsTypeEnum.SET_JSON.value,
                       payload={"key": key, "value": value, "path": path})

    @staticmethod
    def handle_missing_account_details(account_ids, db_session, cache_conn):
        """This method is used to handle the missing account details
        - Get data from sql
        - Prepare payload
        - Sync Data into the Redis

        :return: Missing account details
        """

        missing_account_details = {}

        if account_ids:
            mysql_data = GetMultipleAccountDetails.get_data_from_sql(db_session, account_ids)
            for account_detail in mysql_data:
                account_id = account_detail['account_id']
                key = RedisKeyEnum.ACCOUNT_DATA.value.format(account_id=account_id)
                GetMultipleAccountDetails.set_data_in_cache(cache_conn, key, account_detail)
                missing_account_details[str(account_id)] = account_detail
        return missing_account_details


class GetOutboundMessagesRemainingBalance(Getter):
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
            outbound_messages_total_balance = get_outbound_messages_total_balance(conn=db_conn,
                                                                                  account_id=kwargs.get("account_id"))

        if outbound_messages_total_balance:
            return dict(outbound_messages_total_balance=outbound_messages_total_balance)
        add_log(logger, "No outbound messages found for account {account_id} in SQL database".format(
            account_id=kwargs.get("account_id")))

    @staticmethod
    def get_data_from_elasticsearch(logger=None, **kwargs):
        """
        Its overriding base class method ``get_data_from_elasticsearch``.
        """
        if kwargs.get("db_data"):
            return {"used_outbound_messages": get_used_outbound_messages_balance(
                account_id=kwargs.get("account_id"),
                start_date=str_datetime(kwargs.get("db_data").get("outbound_messages_total_balance").start_at, DT_FMT_Ymd),
                end_date=str_datetime(kwargs.get("db_data").get("outbound_messages_total_balance").end_at, DT_FMT_Ymd))}
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

        :return: Remaining outbound messages
        """

        return str(data.get("outbound_messages_total_balance").config.get("max_outbound_messages", 0) - es_result.get("used_outbound_messages", 0))


@SingletonDecorator
class ManageDeleteAccountResource:
    """
    This class is used to manage the Conversation operations.

    Conversation Get methods will follow below process.
        1. Get data from Cache
    """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_ongoing_resource(self, account_id):
        """ This method is used to get the last in-process resource of the account deletion process """

        resources = GetDeleteAccountResource().get_ongoing_resource_from_sql(self.config.db_session, account_id)
        for key, value in resources.items():
            if value == IN_PROGRESS:
                return key
            elif value == DELETED and value != RESOURCES[-1]:
                return RESOURCES[RESOURCES.index(key) + 1]
            elif value == DELETED and value == RESOURCES[-1]:
                return None
        return RESOURCES[0]

    def is_resource_stats_tracked(self, account_id, stats):
        """ This method is used to check the resource is tracked or not ?? """
        resource = GetDeleteAccountResource().get_resource_stats_from_sql(self.config.db_session, account_id, stats)
        return resource


class GetDeleteAccountResource(Getter):

    @staticmethod
    def get_ongoing_resource_from_sql(db_session, account_id):
        """
        This method is used to fetch data from the SQL database.

        Required parameters:
            :param db_session: <<Class object>>

        Optional Parameters:
            :param account_id: Account Unique ID

        :return: Data if found else empty object {}
        """
        with SessionHandler(db_session) as db_conn:
            result = get_account_delete_resource(db_conn, account_id)
        if result:
            return result.resources
        return {}

    @staticmethod
    def get_resource_stats_from_sql(db_session, account_id, resource):
        """
        This method is used to fetch data from the SQL database.

        Required parameters:
            :param db_session: <<Class object>>

        Optional Parameters:
            :param account_id: Account Unique ID

        :return: Data if found else empty object {}
        """
        with SessionHandler(db_session) as db_conn:
            result = get_account_resource_stats(db_conn, account_id, resource)
        if result:
            return result.resource
        return {}


class GetAccountIdFromKey:
    def __init__(self):
        self.config = ConnectionNetwork()

    def get_account_id_from_account_key(self, account_key):
        key = RedisKeyEnum.ACCOUNT_KEY_ID_MAPPING.value.format(account_key=account_key)
        data = GetAccountIdFromKey.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)

        if data:
            return int(data)
        else:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger,
                    "Fetching data from SQL database for account key {account_key}".format(account_key=account_key))

            data = SyncDataHandler.sync_data(self.config.db_session, self.config.cache_conn,
                                             GetAccountIdFromKey, key, account_key=account_key, logger=self.config.logger)
            return data

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
            account_id = fetch_account_id_by_account_key(conn=db_conn, account_key=kwargs.get("account_key"))

        if account_id:
            return account_id

        add_log(logger, "No data found for account key {account_key} in SQL database".format(
            account_key=kwargs.get("account_key")))

    @staticmethod
    def get_data_from_elasticsearch(logger=None, **kwargs):
        """
        Its overriding base class method ``get_data_from_elasticsearch``.
        Here we don't require to fetch anything from the elastic search. So it will return an empty object
        """
        return {}

    @staticmethod
    def prepare_sync_payload(account_id, es_result, **kwargs):
        """
        It will prepare payload to add data in Cache storage.
        Required parameters:
            :param account_id: Int
            :param es_result: <<Object>>: Data fetched from the elasticsearch
        :return: Object
        """
        return account_id
