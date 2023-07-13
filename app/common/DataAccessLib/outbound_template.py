from CachingLib import RedisOperationsTypeEnum

from DataAccessLib.common.enum import RedisKeyEnum
from DataAccessLib.common.utility import add_log, SingletonDecorator
from DataAccessLib.connection_network import ConnectionNetwork
from DataAccessLib.database.MySQL.outbound_templates import get_outbound_templates
from DataAccessLib.database.connect import SessionHandler
from DataAccessLib.handler import Getter, SyncDataHandler


@SingletonDecorator
class ManageTemplates:
    """
    This class is used to manage the outbound template.

     Get Team member methods will follow below process.
        1. Get data from Cache
        2. If data not found then Invoke ``sync_data`` method of class "SyncDataHandler" to fetch the data from SQL
        and set in Cache.
    """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_template_details(self, template_id):
        """
        This method is used to fetch outbound template details from cache.

        :param template_id: INTEGER: Unique template ID
        :return: Outbound Template Details
        """

        key = RedisKeyEnum.OUTBOUND_TEMPLATE.value.format(template_id=template_id)
        data = GetOutboundTemplateDetails.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger,
                    "Fetching data from SQL database for template: {template_id}".format(template_id=template_id))

            data = SyncDataHandler.sync_data(
                self.config.db_session,
                self.config.cache_conn,
                GetOutboundTemplateDetails,
                key,
                template_id=template_id,
                logger=self.config.logger
            )
        return data


class GetOutboundTemplateDetails(Getter):
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
            template = get_outbound_templates(conn=db_conn, template_id=kwargs.get("template_id"))
        if template:
            return template
        add_log(logger, "No data for template {template_id} in SQL database".format(
            template_id=kwargs.get("template_id")))

    @staticmethod
    def get_data_from_elasticsearch(logger=None, **kwargs):
        """
        Its overriding base class method ``get_data_from_elasticsearch``. Here we don't require to fetching anything
        from the ElasticSearch, so it will return empty object
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

        return dict(
            template_name=data.name,
            template_id=data.template_id,
            channel_id=data.channel_id,
            channel_configuration_id=data.channel_configuration_id,
            status=data.status,
            category=data.category,
            channel_provider_id=data.channel_provider_id,
            template_configuration=data.configurations,
            components=data.components,
            media_id=data.media_id
        )
