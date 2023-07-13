from CachingLib import RedisOperationsTypeEnum

from DataAccessLib.common.enum import RedisKeyEnum
from DataAccessLib.common.utility import add_log, SingletonDecorator
from DataAccessLib.connection_network import ConnectionNetwork
from DataAccessLib.database.MySQL.account import get_account_bots
from DataAccessLib.database.MySQL.conversation import get_conversation_count_between_date_range
from DataAccessLib.database.MySQL.conversation_audit_balance import (get_subscription_start_at_and_end_at)
from DataAccessLib.database.connect import SessionHandler
from DataAccessLib.handler import Getter, SyncDataHandler


@SingletonDecorator
class ManageAccountConversationBalanceAudit:
    """
    This class is used to manage the account conversation audit operations. It has different type of Get methods to
     fetch the data.

    Account Get methods will follow below process.
        1. Get data from Cache
        2. If data not found then Invoke ``sync_data`` method of class "SyncDataHandler" to fetch the data from SQL
        and set in Cache.
    """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_account_conversation_remaining_balance(self, account_id):
        """
        This method is used to fetch account conversation remaining balance.

        :param account_id: INTEGER: Unique account id
        :return: Account remaining conversation balance if data found in Cache or SQL database else empty response
        """

        key = RedisKeyEnum.ACCOUNT_CONVERSATION_REMAINING_BALANCE.value.format(account_id=account_id)
        data = GetAccountConversationRemainingBalance.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger,
                    "Fetching data from SQL database for account {account_id}".format(account_id=account_id))

            data = SyncDataHandler.sync_data(self.config.db_session, self.config.cache_conn,
                                             GetAccountConversationRemainingBalance, key,
                                             logger=self.config.logger, account_id=account_id)
        return data


class GetAccountConversationRemainingBalance(Getter):
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
        account_bots = []
        with SessionHandler(db_session) as db_conn:
            start_at_and_end_at = get_subscription_start_at_and_end_at(conn=db_conn,
                                                                       account_id=kwargs.get("account_id"))
            if start_at_and_end_at:
                start_at = start_at_and_end_at.start_at
                end_at = start_at_and_end_at.end_at
                credited_conversation_balance = db_conn.execute(
                    'CALL sp_get_account_conversation_balance("{start_at}", "{end_at}", {account_id})'.format(
                        start_at=start_at,
                        end_at=end_at,
                        account_id=kwargs.get("account_id")
                    ))
                conversation_balance = credited_conversation_balance.fetchall()[0].conversation_balance
                conversation_balance = int(conversation_balance) if conversation_balance else None
                if conversation_balance:
                    account_bot_list = get_account_bots(conn=db_conn, account_id=kwargs.get("account_id"))
                    if account_bot_list:
                        account_bots = [int(bot.id) for bot in account_bot_list]
                    count = get_conversation_count_between_date_range(conn=db_conn, start_at=start_at,
                                                                      end_at=end_at, bots=account_bots).count
                    if count:
                        conversation_balance -= count
                    return dict(conversation_balance=conversation_balance)

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

        conversation_balance = data.get("conversation_balance")
        return conversation_balance
