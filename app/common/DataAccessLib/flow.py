import json

from CachingLib import RedisOperationsTypeEnum

from DataAccessLib.common.enum import RedisKeyEnum
from DataAccessLib.common.utility import add_log, SingletonDecorator
from DataAccessLib.connection_network import ConnectionNetwork
from DataAccessLib.database.MySQL.flow import get_dialog_feature_mapping_data
from DataAccessLib.database.connect import SessionHandler
from DataAccessLib.handler import Getter, SyncDataHandler


@SingletonDecorator
class ManageFlow:
    """
    This class is used to manage the flow operations. It has different type of Get methods to fetch the flow
    related data.

    Flow Get methods will follow below process.
        1. Get data from Cache
        2. If data not found then Invoke ``sync_data`` method of class "SyncDataHandler" to fetch the data from SQL
        and set in Cache.
    """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_dialog_feature_mapping(self):
        """
        This method is used to fetch the dialog <-> feature mapping.

        :return: Dialog <-> Features Mapping if data found in Cache or SQL database else empty response
        """

        key = RedisKeyEnum.DIALOG_FEATURE_MAPPING.value
        data = GetFlowDetails.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger,
                    "Fetching data from SQL database for bot_builder_block_feature_mapping")

            data = SyncDataHandler.sync_data(self.config.db_session, self.config.cache_conn,
                                             GetFlowDetails, key, logger=self.config.logger)
        return data


class GetFlowDetails(Getter):
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

        :return: Data if found else empty list []
        """
        with SessionHandler(db_session) as db_conn:
            mapping_data = get_dialog_feature_mapping_data(conn=db_conn)
        if mapping_data:
            return mapping_data
        add_log(logger, "No data for bot_builder_block_feature_mapping in SQL database")
        return []

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
        payload = {}

        for mapping_data in data:
            if mapping_data.bot_builder_block_key not in payload:
                payload[mapping_data.bot_builder_block_key] = {'id': mapping_data.bot_builder_block_id, 'features': {}}
            payload[mapping_data.bot_builder_block_key]['features'][mapping_data.feature_key] = {'id': mapping_data.feature_id}

        return payload
