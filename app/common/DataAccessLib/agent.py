from CachingLib import RedisOperationsTypeEnum

from DataAccessLib.common.enum import RedisKeyEnum, AgentTrackingFields
from DataAccessLib.common.utility import add_log, SingletonDecorator, remove_none_from_list
from DataAccessLib.connection_network import ConnectionNetwork
from DataAccessLib.database.MySQL.agent import (get_agent_details, get_agent_roles, get_agent_status,
                                                get_multiple_agent_details, get_user_preferences,
                                                get_user_notification_tokens, get_user_notification_preferences)
from DataAccessLib.database.connect import SessionHandler
from DataAccessLib.handler import Getter, SyncDataHandler
from UtilsLib import decode_unicode


@SingletonDecorator
class ManageAgent:
    """
    This class is used to manage the agent operations. It has different type of Get methods to fetch the agent related
    data.

    Bot Get methods will follow below process.
        1. Get data from Cache
        2. If data not found then Invoke ``sync_data`` method of class "SyncDataHandler" to fetch the data from SQL
        and set in Cache.
    """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_agent_details(self, agent_id):
        """
        This method is used to fetch agent details.

        :param agent_id: INTEGER: Unique agent id
        :return: Agent data if data found in Cache or SQL database else empty response
        """

        key = RedisKeyEnum.AGENT_DATA.value.format(agent_id=agent_id)
        data = GetAgentDetails.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger,
                    "Fetching data from SQL database for Agent {agent_id}".format(agent_id=agent_id))

            data = SyncDataHandler.sync_data(self.config.db_session, self.config.cache_conn,
                                             GetAgentDetails, key, agent_id=agent_id, logger=self.config.logger)
        return data

    def get_agent_roles(self, agent_id):
        """
        This method is used to fetch agent roles.

        :param agent_id: INTEGER: Unique agent id
        :return: Agent roles if data found in Cache or SQL database else empty response
        """

        key = RedisKeyEnum.AGENT_ROLE.value.format(agent_id=agent_id)
        data = GetAgentRoles.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger,
                    "Fetching data from SQL database for Agent {agent_id}".format(agent_id=agent_id))

            data = SyncDataHandler.sync_data(self.config.db_session, self.config.cache_conn,
                                             GetAgentRoles, key, agent_id=agent_id, logger=self.config.logger)
        return data

    def get_multiple_agent_details(self, agent_ids):
        """This method is used to fetch multiple agents details"""
        keys = [RedisKeyEnum.AGENT_DATA.value.format(agent_id=agent_id) for agent_id in agent_ids]
        data = GetMultipleAgentDetails.get_data_from_cache(cache_conn=self.config.cache_conn, keys=keys)
        data = remove_none_from_list(data)
        data = [{key: decode_unicode(value) if isinstance(value, str) else value
                 for key, value in item.items()} for item in data]

        missing_agent_ids = GetMultipleAgentDetails.get_missing_agent_ids(data, agent_ids)

        missing_agents_data = GetMultipleAgentDetails.handle_missing_agents(missing_agent_ids, self.config.db_session,
                                                                            self.config.cache_conn)

        return data + missing_agents_data

    def get_user_preferences(self, user_id):
        """This method is used to fetch user preferences

        :param user_id: INTEGER: Unique user id
        :return: user preferences if data found in Cache or SQL database else empty response
        """

        key = RedisKeyEnum.USER_PREFERENCE.value.format(user_id=user_id)
        data = GetUserPreferences.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger,
                    "Fetching user preference from SQL database for user_id {user_id}".format(user_id=user_id))

            data = SyncDataHandler.sync_data(self.config.db_session, self.config.cache_conn,
                                             GetUserPreferences, key, user_id=user_id, logger=self.config.logger)
        return data

    def get_user_notification_preferences(self, recipients):
        """This method is used to fetch user notification preferences

        :param recipients: LIST<INTEGER>: Unique user id list
        :return: user notification preferences
        """
        get_data_handler = GetUserNotificationPreferences()
        mysql_result = get_data_handler.get_data_from_sql(self.config.db_session, recipients=recipients)
        user_notification_preferences = []
        if mysql_result:
            user_notification_preferences = [
                {
                    "user_id": data.user_id,
                    "notification_events": data.notification_events
                } for data in mysql_result['user_notification_preferences']
            ]
        data = {
            'user_notification_preferences': user_notification_preferences
        }
        return get_data_handler.prepare_sync_payload(data=data, es_result=None)

    def get_user_notification_tokens(self, recipients, _type):
        """This method is used to fetch user notification tokens

        :param recipients: LIST<INTEGER>: Unique user id list
        :params _type: PWA or react-native
        :return: user notification tokens
        """

        get_data_handler = GetUserNotificationTokens()
        mysql_result = get_data_handler.get_data_from_sql(self.config.db_session, recipients=recipients, _type=_type)
        user_notification_tokens = []
        if mysql_result:
            user_notification_tokens = [data.token for data in mysql_result['user_notification_tokens']]
        data = {
            'user_notification_tokens': user_notification_tokens
        }
        return get_data_handler.prepare_sync_payload(data=data, es_result=None)


class GetAgentDetails(Getter):
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

        :return: Data if found else None
        """
        with SessionHandler(db_session) as db_conn:
            agent_data = get_agent_details(conn=db_conn, agent_id=kwargs.get("agent_id"))
        if agent_data:
            return dict(agent_data=agent_data)
        add_log(logger, "No data for agent {agent_id} in SQL database".format(agent_id=kwargs.get("agent_id")))

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

        agent_data = data.get("agent_data")
        first_name = agent_data.first_name if agent_data.first_name else ''
        last_name = agent_data.last_name if agent_data.last_name else ''
        return dict(email=agent_data.email,
                    id=agent_data.id,
                    first_name=first_name,
                    last_name=last_name,
                    image_name=agent_data.image_name,
                    user_type_id=agent_data.user_type_master_id)


class GetAgentRoles(Getter):
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

        :return: Data if found else None
        """
        with SessionHandler(db_session) as db_conn:
            agent_roles = get_agent_roles(conn=db_conn, agent_id=kwargs.get("agent_id"))
            agent_status = get_agent_status(conn=db_conn, agent_id=kwargs.get("agent_id"))
        if agent_status and agent_roles:
            return dict(agent_roles=agent_roles, agent_status=agent_status)
        add_log(logger, "No roles found for agent {agent_id} in SQL database".format(agent_id=kwargs.get("agent_id")))

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

        agent_roles = data.get("agent_roles")
        agent_status = data.get("agent_status")

        bots_list = {}
        accounts_list = {}

        for item in agent_roles:
            bot_id = AgentTrackingFields.BOT_ID.value.format(bot_id=item.bot_id)
            bots_list[bot_id] = {"role": item.user_role_master_id}
            account_id = AgentTrackingFields.ACCOUNT_ID.value.format(account_id=item.account_id)
            accounts_list[account_id] = {"role": item.user_role_master_id}

        return {AgentTrackingFields.STATUS_ID.value: agent_status.user_status_master_id,
                AgentTrackingFields.ACCESS.value: {"accounts": accounts_list}}


class GetMultipleAgentDetails:
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
    def get_missing_agent_ids(data, agent_ids):
        """This method is used to get the missing agent ids which is not presents in the cache"""

        if len(data) != len(agent_ids):
            available_agent_ids = [agent['id'] for agent in data]
            return list(set(agent_ids) - set(available_agent_ids))

        return []

    @staticmethod
    def handle_missing_agents(agent_ids, db_session, cache_conn):
        """This method is used to handle the missing agents details
        - Get data from sql
        - Prepare payload
        - Sync Data into the Redis

        :return: Missing agent details
        """

        missing_agent_details = []

        if agent_ids:
            data = GetMultipleAgentDetails.get_data_from_sql(db_session, agent_ids)

            for agent_data in data:
                sync_payload = GetMultipleAgentDetails.prepare_sync_payload(agent_data)
                key = RedisKeyEnum.AGENT_DATA.value.format(agent_id=agent_data.id)
                GetMultipleAgentDetails.set_data_in_cache(cache_conn, key, sync_payload)

                missing_agent_details.append(sync_payload)

        return missing_agent_details

    @staticmethod
    def get_data_from_sql(db_session, agent_ids):
        """
        This method is used to fetch data from the SQL database.

        Required parameters:
            :param db_session: <<Class object>>
            :param agent_ids: List


        :return: Data if found else empty list
        """
        with SessionHandler(db_session) as db_conn:
            agent_data = get_multiple_agent_details(conn=db_conn, agent_ids=agent_ids)
        if agent_data:
            return agent_data

        return []

    @staticmethod
    def prepare_sync_payload(agent_data):
        """
        It will prepare payload to add data in Cache storage.

        Required parameters:
            :param agent_data: <<Class object>>: Data fetched from the SQL

        :return: Object
        """

        first_name = agent_data.first_name if agent_data.first_name else ''
        last_name = agent_data.last_name if agent_data.last_name else ''
        return dict(email=agent_data.email,
                    id=agent_data.id,
                    first_name=first_name,
                    last_name=last_name,
                    image_name=agent_data.image_name,
                    user_type_id=agent_data.user_type_master_id)

    @staticmethod
    def set_data_in_cache(cache_conn, key, value, path="."):

        cache_conn.set(operation_type=RedisOperationsTypeEnum.SET_JSON.value,
                       payload={"key": key, "value": value, "path": path})


class GetUserPreferences(Getter):
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

        :return: Data if found else None
        """
        with SessionHandler(db_session) as db_conn:
            user_preferences = get_user_preferences(db_conn, kwargs.get("user_id"))
        if user_preferences:
            return dict(user_preferences=user_preferences)

        add_log(logger, "No user preferences found for user {user_id} in SQL database".format(
            user_id=kwargs.get("user_id")))

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

        return data.get("user_preferences").preferences


class GetUserNotificationPreferences(Getter):
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

        :return: Data if found else None
        """
        with SessionHandler(db_session) as db_conn:
            user_notification_preferences = get_user_notification_preferences(db_conn, kwargs.get("recipients"))
        if user_notification_preferences:
            return dict(user_notification_preferences=user_notification_preferences)

        add_log(logger, "No user notification preferences found for recipients: {recipients} in SQL database".format(
            recipients=kwargs.get("recipients")))

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

        return dict(user_notification_preferences=data.get("user_notification_preferences"))


class GetUserNotificationTokens(Getter):
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

        :return: Data if found else None
        """
        with SessionHandler(db_session) as db_conn:
            user_notification_tokens = get_user_notification_tokens(db_conn, kwargs.get("recipients"),
                                                                    kwargs.get("_type"))
        if user_notification_tokens:
            return dict(user_notification_tokens=user_notification_tokens)

        add_log(logger, "No user notification tokens found for recipients: {recipients} in SQL database".format(
            recipients=kwargs.get("recipients")))

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

        return dict(user_notification_tokens=data.get("user_notification_tokens"))
