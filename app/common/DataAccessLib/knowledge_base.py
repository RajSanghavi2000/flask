from CachingLib import RedisOperationsTypeEnum
from DataAccessLib.common.enum import RedisKeyEnum
from DataAccessLib.common.utility import add_log, SingletonDecorator
from DataAccessLib.connection_network import ConnectionNetwork
from DataAccessLib.database.MySQL.knowledge_base import get_knowledge_base_details
from DataAccessLib.database.connect import SessionHandler
from DataAccessLib.handler import Getter, SyncDataHandler


@SingletonDecorator
class ManageFAQKnowledgeBase:
    """
    This class is used to manage the FAQ knowledge base operations. It has different type of Get methods to fetch the
    knowledge base related data.

    Knowledge base Get methods will follow below process.
        1. Get data from Cache
        2. If data not found then Invoke ``sync_data`` method of class "SyncDataHandler" to fetch the data from SQL
        and set in Cache.
    """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_knowledge_base_details(self, knowledge_base_id):
        """
        This method is used to fetch knowledge base details.

        :param knowledge_base_id: INTEGER: Unique knowledge base id
        :return: Knowledge base data if data found in Cache or SQL database else empty response
        """

        key = RedisKeyEnum.KNOWLEDGE_BASE.value.format(knowledge_base_id=knowledge_base_id)
        data = GetKnowledgeBaseDetails.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger, "Fetching data from SQL database for knowledge base {knowledge_base_id}".format(knowledge_base_id=knowledge_base_id))

            data = SyncDataHandler.sync_data(
                self.config.db_session, self.config.cache_conn,
                GetKnowledgeBaseDetails, key, knowledge_base_id=knowledge_base_id, logger=self.config.logger
            )
        return data


class GetKnowledgeBaseDetails(Getter):
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
            knowledge_base_data = get_knowledge_base_details(conn=db_conn, knowledge_base_id=kwargs.get("knowledge_base_id"))
        if knowledge_base_data:
            return knowledge_base_data
        add_log(logger, "No data for knowledge base {knowledge_base_id} in SQL database".format(knowledge_base_id=kwargs.get("knowledge_base_id")))

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

        return dict(account_id=data.account_id, status=data.status, configurations=data.configurations,
                    trained_model=data.trained_model, type=data.type)

