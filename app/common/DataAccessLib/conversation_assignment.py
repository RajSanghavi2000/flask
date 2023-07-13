from CachingLib import RedisOperationsTypeEnum

from DataAccessLib.common.enum import RedisKeyEnum
from DataAccessLib.common.utility import add_log, SingletonDecorator
from DataAccessLib.connection_network import ConnectionNetwork
from DataAccessLib.database.MySQL.account import (get_account_users, get_account_bots)
from DataAccessLib.database.MySQL.conversation_assignment import (get_user_workload_by_account_id)
from DataAccessLib.database.connect import SessionHandler
from DataAccessLib.handler import Getter, SyncDataHandler


@SingletonDecorator
class ManageConversationAssignment:
    """
    This class is used to manage the conversation assignment operations. It has different type of Get methods to fetch
    the conversation assignment related data.

    Conversation assignment Get methods will follow below process.
        1. Get data from Cache
        2. If data not found then Invoke ``sync_data`` method of class "SyncDataHandler" to fetch the data from SQL
        and set in Cache.
    """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_conversation_assignment_details(self, account_id):
        """
        This method is used to fetch conversation assignment details.

        :param account_id: INTEGER: Unique bot id
        :return: Conversation assignment data if data found in Cache or SQL database else empty response
        """

        key = RedisKeyEnum.CONVERSATION_ASSIGNMENT_DATA.value.format(account_id=account_id)
        data = GetConversationAssignmentDetails.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger, "Fetching data from SQL database for account {account_id}".format(
                account_id=account_id))

            data = SyncDataHandler.sync_data(
                self.config.db_session, self.config.cache_conn,
                GetConversationAssignmentDetails, key, account_id=account_id, logger=self.config.logger
            )
        return data


class GetConversationAssignmentDetails(Getter):
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
        db_conversation_assignments = []
        account_users = []
        conversation_assignments = []
        assign_users = []
        account_bots = []
        with SessionHandler(db_session) as db_conn:
            account_user_list = get_account_users(conn=db_conn, account_id=kwargs.get("account_id"))
            if account_user_list:
                account_users = [int(user.id) for user in account_user_list]
            account_bot_list = get_account_bots(conn=db_conn, account_id=kwargs.get("account_id"))
            if account_bot_list:
                account_bots = [int(bot.id) for bot in account_bot_list]
        if account_users and account_bots:
            db_conversation_assignments = get_user_workload_by_account_id(conn=db_conn, bots=account_bots,
                                                                          users=account_users)
        if db_conversation_assignments:
            for conversation_assignment in db_conversation_assignments:
                user_id = conversation_assignment[0]
                conversation_ids = conversation_assignment[1].split(',') if conversation_assignment[1] else []
                assign_conversations = list(map(int, conversation_ids))
                conversation_assignments.append({
                    "user_id": user_id,
                    "assign_threads": assign_conversations
                })
                assign_users.append(user_id)
        GetConversationAssignmentDetails.order_user_assignment(account_users,
                                                               assign_users,
                                                               conversation_assignments)
        if conversation_assignments:
            return dict(conversation_assignments=conversation_assignments)
        add_log(logger, "No data for account_id {account_id} in SQL database".format(
            account_id=kwargs.get("account_id")))

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
        return data['conversation_assignments']

    @staticmethod
    def order_user_assignment(account_users, assign_users, conversation_assignments):

        def _order_list(users):
            if users:
                users.reverse()
                for user_id in users:
                    conversation_assignments.insert(0, {"user_id": user_id, "assign_threads": []})

        if account_users:
            if assign_users:
                unassigned_users = [aid for aid in account_users if aid not in assign_users]
                _order_list(unassigned_users)
            else:
                _order_list(account_users)
