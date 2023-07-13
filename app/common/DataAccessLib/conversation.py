from DataAccessLib.handler import Getter
from CachingLib import RedisOperationsTypeEnum
from DataAccessLib.common.enum import (RedisKeyEnum)
from DataAccessLib.common.utility import SingletonDecorator
from DataAccessLib.connection_network import ConnectionNetwork
from DataAccessLib.database.connect import SessionHandler
from DataAccessLib.database.MySQL.conversation import get_account_total_conversation_count


@SingletonDecorator
class ManageConversation:
    """
    This class is used to manage the Conversation operations.

    Conversation Get methods will follow below process.
        1. Get data from Cache
    """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_conversation(self, key=''):
        """
        This method is used to get conversation object

        :param key: STRING: Unique key assigned to every conversation
        """

        conversation = {}
        if key:
            conversation = self.__get_conversation_by_conversation_key(key)

        return conversation if conversation else {}

    def __get_conversation_by_conversation_key(self, conversation_key):
        """
        This method is used to get conversation object using conversation key

        :param key: STRING: Unique key assigned to every conversation
        """
        key = RedisKeyEnum.CONVERSATION.value.format(conversation_key=conversation_key)
        conversation = GetConversationByConversationKey.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        return conversation

    def get_account_total_conversation_count(self, account_id):
        """ This method is used to get account total conversation count """

        return GetConversationByConversationKey().get_account_total_conversations_count(self.config.db_session,
                                                                                        account_id)


class GetConversationByConversationKey(Getter):
    @staticmethod
    def get_data_from_cache(cache_conn, key, **kwargs):
        """
        It's overriding base class method ``get_data_from_cache`` and fetch bot data from the Cache database. It's using ``GetData``
        class of ``caching`` package to perform this operation.
        """

        conversation = cache_conn.get(operation_type=RedisOperationsTypeEnum.GET_JSON.value, payload={"key": key})

        return conversation

    @staticmethod
    def get_account_total_conversations_count(db_session, account_id):
        """ Get conversations count from the MySQL """

        with SessionHandler(db_session) as db_conn:
            result = get_account_total_conversation_count(db_conn, account_id)
        return result.count
