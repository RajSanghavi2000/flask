from CachingLib import RedisOperationsTypeEnum
from DataAccessLib.connection_network import ConnectionNetwork

from DataAccessLib.common.enum import RedisKeyEnum
from DataAccessLib.database.MySQL.labels import (get_account_labels)
from DataAccessLib.common.utility import add_log, SingletonDecorator
from DataAccessLib.database.connect import SessionHandler
from DataAccessLib.handler import Getter, SyncDataHandler


@SingletonDecorator
class ManageAccountLabels:
    """
    This class is used to manage the account variables. It has different type of Get methods to fetch the label related data.
    Get variable methods will follow below process.
        1. Get data from Cache
        2. If data not found then Invoke ``sync_data`` method of class "SyncDataHandler" to fetch the data from SQL
        and set in Cache.
    """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_account_labels(self, account_id):
        """
        This method is used to fetch labels.

        :param account_id: INTEGER: Unique account id
        :return: label format data if data found in Cache or SQL database else empty response
        """

        key = RedisKeyEnum.ACCOUNT_LABELS.value.format(account_id=account_id)
        data = GetLabels.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger,
                    "Fetching data from SQL database for variable {account_id}".format(account_id=account_id))

            data = SyncDataHandler.sync_data(
                self.config.db_session, self.config.cache_conn,
                GetLabels, key, account_id=account_id, logger=self.config.logger
            )
        return data


class GetLabels(Getter):
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
            labels_data = get_account_labels(conn=db_conn, account_id=kwargs.get("account_id"))
        if labels_data:
            return dict(labels_data=labels_data)
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

        labels_data = data.get('labels_data')
        return [dict(id=label_data.id,
                    label=label_data.label,
                    created_by=label_data.created_by,
                    created_at=str(label_data.created_at)) for label_data in labels_data]
