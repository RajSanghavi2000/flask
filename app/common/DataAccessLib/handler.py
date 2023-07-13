from CachingLib import RedisOperationsTypeEnum


class Getter:
    """
    Base method to handle GetData operations. It has have ``get_data_from_cache``, ``get_data_from_sql``,
    ``prepare_sync_payload`` method. It will be override by the child class
    """

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
        pass

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

        pass

    @staticmethod
    def get_data_from_elasticsearch(logger=None, **kwargs):
        """
        This method is used to fetch data from the elasticsearch

        Optional Parameters:
            :param logger: <<Class object>>
            :param kwargs: Extra arguments

        :return: Data if found else empty object {}
        """
        pass

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
        pass


class SyncDataHandler:
    """
    It is a handler class to SyncData into the Cache database by fetching first from the SQL database.
    - It has ``sync_data`` and ``_set_data_in_cache`` methods.
    ``sync_data``: Can be use by any method to sync data into the Cache database
    ``_set_data_in_cache`` : Used by ``sync_data`` method to set data into the Cache storage

    """

    @staticmethod
    def sync_data(db_session, cache_conn, get_data_handler, key, logger="", **kwargs):
        """
        It's a handle method to handle sync data operations. It follows the below process.
            Step 1. Fetch data from SQL and elasticsearch
            Step 2. If data found then go to step 3 else go to step 6
            Step 3. Convert fetch data into the specific format
            Step 4. Store data into the Cache database
            Step 5: Return requested data
            Step 6: Return empty object

        Required parameters:
            :param db_session: <<Class object>>: SQL Database session object to create connection
            :param cache_conn: <<Class object>>: Cache Database connection object
            :param get_data_handler: <<Class>>: Handle Class to get the data
            :param key: STRING: Key under which data will be stored in Cache storage

        Optional parameters:
            :param logger: <<Class object>>: Logger object
            :param kwargs: Extra arguments

        :return: Data if found else empty object {}
        """

        data = get_data_handler.get_data_from_sql(db_session, logger, **kwargs)
        es_result = get_data_handler.get_data_from_elasticsearch(logger, db_data=data, **kwargs)

        if not data and not es_result:
            return {}

        kwargs['db_session'] = db_session
        kwargs['cache_conn'] = cache_conn
        payload = get_data_handler.prepare_sync_payload(data, es_result, **kwargs)
        result = SyncDataHandler._set_data_in_cache(cache_conn=cache_conn, key=key, value=payload)
        if kwargs.get("redis_key_expire_time"):
            SyncDataHandler._set_redis_key_expire(cache_conn=cache_conn, key=key, expire_time=kwargs.get(
                "redis_key_expire_time"))
        return result

    @staticmethod
    def _set_data_in_cache(cache_conn, key, value, path="."):
        if isinstance(value, str) or isinstance(value, int):
            cache_conn.set(operation_type=RedisOperationsTypeEnum.SET.value,
                           payload={"key": key, "value": value})
        else:
            cache_conn.set(operation_type=RedisOperationsTypeEnum.SET_JSON.value,
                           payload={"key": key, "value": value, "path": path})
        return value

    @staticmethod
    def _set_redis_key_expire(cache_conn, key, expire_time):
        cache_conn.set(operation_type=RedisOperationsTypeEnum.SET_EXPIRY_TIME.value,
                           payload={"key": key, "expire_time": expire_time})
