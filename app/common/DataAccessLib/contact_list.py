from CachingLib import RedisOperationsTypeEnum

from DataAccessLib.common.enum import RedisKeyEnum
from DataAccessLib.common.utility import add_log, SingletonDecorator
from DataAccessLib.connection_network import ConnectionNetwork
from DataAccessLib.database.MySQL.account import get_contact_lists
from DataAccessLib.database.connect import SessionHandler
from DataAccessLib.handler import Getter, SyncDataHandler


@SingletonDecorator
class ManageContactList:
    """
    This class is used to manage the contact list operations. It has different type of Get methods to fetch the contact
    list related data.

     Get Contact lists methods will follow below process.
        1. Get data from Cache
        2. If data not found then Invoke ``sync_data`` method of class "SyncDataHandler" to fetch the data from SQL
        and set in Cache.
    """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_contact_lists(self, account_id):
        """
        This method is used to fetch contact lists.

        :param account_id: INTEGER: Unique account id
        :return: Contact list data if data found in Cache or SQL database else empty response
        """

        key = RedisKeyEnum.CONTACT_LISTS.value.format(account_id=account_id)
        data = GetContactLists.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger,
                    "Fetching data from SQL database for account: {account_id}".format(account_id=account_id))

            data = SyncDataHandler.sync_data(self.config.db_session, self.config.cache_conn,
                                             GetContactLists, key, account_id=account_id, logger=self.config.logger)
        return data


class GetContactLists(Getter):
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
        contact_lists = []
        with SessionHandler(db_session) as db_conn:
            contact_list = get_contact_lists(conn=db_conn, account_id=kwargs.get("account_id"))
        if contact_list:
            for member in contact_list:
                contact_lists.append({"id": member.id,"name": member.name,"is_editable": member.is_editable,
                                      "is_deleted": member.is_deleted})
            return dict(contact_lists=contact_lists)
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

        contact_lists = data.get("contact_lists")
        return contact_lists
