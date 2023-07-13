import json
import re

from CachingLib import RedisOperationsTypeEnum

from DataAccessLib.database.connect import SessionHandler
from DataAccessLib.handler import Getter, SyncDataHandler
from DataAccessLib.common.enum import RedisKeyEnum
from DataAccessLib.common.utility import SingletonDecorator, add_log
from DataAccessLib.connection_network import ConnectionNetwork
from DataAccessLib.database.MySQL.addons import (
    get_addons_data,
    get_addon_version_id_and_connected_addon_auth_id,
    get_connected_addon_parameters,
    get_addon_auth_parameters,
    get_addon_functions,
    get_addon_version_id_for_the_function_name,
    get_connected_addon_third_party_variable_mapping,
    get_connected_addon_details_by_webhook_key
)


@SingletonDecorator
class ManageAddons:
    """
    Manage Addons

    Available Methods:
        - Get Addons data from Redis cache
    """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_addons(self, keys: list, function_name: str) -> dict:
        """
        Get Addons object

        :param keys: Unique keys assigned to every Addons
        @type keys: list
        :param function_name: Unique function_name
        @type function_name: str
        @return functions_data Object
        ---------------
        Example Object:
        ---------------
            {
                "addons_key": "0bac570ca67911ebaa6a51d0ce12be38",
                "function_name": "AskEmail",
                "script": ask_email,
                "parameter": {
                    "¿·emailType·?": "business"
                },
                "script_language": "JavaScript"
            }
        """
        functions_data = {}

        for addons_key in keys:
            if functions_data:
                continue
            addons_data = self.__get_addons_by_key(addons_key)
            if not addons_data:
                # Goes to MySQL to get Addons Data
                add_log(self.config.logger,
                        "Addons Data for key `{key}` not found in cache".format(
                            key=addons_key))
                add_log(self.config.logger,
                        "Fetching data from SQL database for Addon "
                        "redis_key {key}".format(key=addons_key))
                addons_data = SyncDataHandler.sync_data(
                    self.config.db_session,
                    self.config.cache_conn,
                    GetAddonsByKey,
                    addons_key,  # connected_addon.redis_key
                    logger=self.config.logger,
                    redis_key=addons_key
                )
            # filter and get function
            functions_data = functions_data or next(
                (item for item in addons_data['functions'] if item["function_name"] == function_name),
                {}
            )
            if functions_data:
                functions_data["addons_key"] = addons_key

        return functions_data

    def __get_addons_by_key(self, addons_key: str):
        """
        This method is used to get addons object using key
        :param addons_key: STRING: Unique key assigned to every Addons
        """
        key = RedisKeyEnum.ADDONS_KEY.value.format(addons_key=addons_key)
        addons = GetAddonsByKey.get_data_from_cache(
            cache_conn=self.config.cache_conn,
            key=key
        )
        return addons


class GetAddonsByKey(Getter):

    @staticmethod
    def get_data_from_cache(cache_conn, key: str, **kwargs) -> dict:
        """
        It's overriding base class method ``get_data_from_cache``
        and fetch Addons data from the Cache database.
        It's using ``GetData`` class of ``caching`` package to perform this operation.
        """
        addons = cache_conn.get(
            operation_type=RedisOperationsTypeEnum.GET_JSON.value,
            payload={"key": key}
        )
        return addons

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
            addons_data = get_addons_data(
                conn=db_conn, redis_key=kwargs.get("redis_key")
            )
        if addons_data:
            return dict(addons_data=addons_data)

        add_log(logger,
                "No Addons data found in SQL database for redis_key "
                "{redis_key}".format(redis_key=kwargs.get("redis_key")))

    @staticmethod
    def get_data_from_elasticsearch(logger=None, **kwargs):
        """
        Its overriding base class method ``get_data_from_elasticsearch``.
        Here we don't require to fetch anything from the elastic search so
        it will return empty object
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
        ----------------
        Example Object:
        ----------------
            {
                "addon_version_id": ID,
                "functions": [
                    {
                        "function_name": "AskEmail",
                        "script": ask_email,
                        "parameter": {
                            "¿·emailType·?": "business"
                        },
                        "script_language": "JavaScript"
                    }
                ]
            }
        """
        addons_data = data.get("addons_data")
        final_data = dict(
            functions=[],
            addon_version_id=None
        )
        for addon in addons_data:
            function_data = GetAddonsByKey.get_function_data(addon)
            final_data['functions'].append(function_data)
            final_data['addon_version_id'] = addon.addon_version_id

        return final_data

    @staticmethod
    def get_function_data(data):
        function_data = dict(
            function_name=data.function_name,
            script=data.script,
            script_language=data.script_language
        )
        function_data['parameter'] = GetAddonsByKey.parse_parameters_from_code(
            function_data['script'], data.auth_parameter
        )
        return function_data

    @staticmethod
    def parse_parameters_from_code(script, auth_parameters):
        """
        core/service/redis_add_on_key_data_mapping_service.py L72
        @param script: Addons Execution Script
        @param auth_parameters: Connected Addon Auth Parameters Json Object
        @return:
        """
        parameter_obj = {}
        parameters = re.findall("¿·(.+?)·\?", script)
        if not isinstance(auth_parameters, dict) or not auth_parameters.get('keys'):
            # auth_parameters can be None when addon doesn't use Oauth
            return parameter_obj
        auth_parameters = json.loads(auth_parameters) if \
            isinstance(auth_parameters, str) else auth_parameters
        for parameter in parameters:
            parameter_key = '¿·' + parameter + '·?'
            parameter_obj[parameter_key] = None
            if parameter in auth_parameters['keys']:
                parameter_obj[parameter_key] = auth_parameters['keys'][parameter]['value']

        return parameter_obj


class GetAddonVersionAndAuthDetails:

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_addon_version_id_and_connected_addon_auth_id(self, function_name, account_id=None):
        """
        Get addon-version-id and connected-addon-auth-id as per provided function-name and account-id.

        Required parameters:
            :param function_name: code-block function name
            :param account_id: id of the particular account

        :return: addon-version-id, connected-addon-auth-id
        """

        with SessionHandler(self.config.db_session) as db_conn:
            if not account_id:
                result = get_addon_version_id_for_the_function_name(
                    conn=db_conn,
                    function_name=function_name
                )

                return result.addon_version_id if result else None, None

            result = get_addon_version_id_and_connected_addon_auth_id(
                conn=db_conn,
                function_name=function_name,
                account_id=account_id
            )

        return result if result else (None, None)


class ManageConnectedAddonAuthParameters:
    """ Manage Connected Addon Auth Parameters """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_connected_addon_auth_parameters(self, connected_addon_auth_id):
        """
        Get connected-addon-connected_addon_auth_id

        Required parameters:
            :param connected_addon_auth_id: connected add on auth id

        :return: connected-addon-auth-id object
        ---------------
        Example Object:
        ---------------
            {
                "keys": {
                    "access_code": {
                        "value": "4/3wHQBBYx2nJcpSp-yZKKQrgTl3-cjTLpsddZeVwovxxjaQdM_HH-0ZudbsAgzVHy4"
                    },
                    "expires_in": {
                        "value": 3599
                    },
                    "access_token": {
                        "value": "ya29.a0AfH6SMAd1XsIs5VdGEPUxhrGqTLTIjF0-4OOWFTbycWBilbiHOdRIXwTIeo"
                    },
                    "refresh_token": {
                        "value": "1//04C6nGLLOYCa5CgUUzJt6xEWXNS-JSiG3HQ9f3UOv7OOoq2Cz53Hra6JV3yCals"
                    }
                }
            }
        """
        key = RedisKeyEnum.CONNECTED_ADDON_AUTH_PARAMETER.value.format(connected_addon_auth_id=connected_addon_auth_id)
        data = GetConnectedAddonAuthParameter.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger,
                    "Fetching data from SQL database for Connected"
                    " Addon Auth Parameter {connected_addon_auth_id}".format(
                        connected_addon_auth_id=connected_addon_auth_id)
                    )
            data = SyncDataHandler.sync_data(
                self.config.db_session,
                self.config.cache_conn,
                GetConnectedAddonAuthParameter,
                key,
                connected_addon_auth_id=connected_addon_auth_id,
                logger=self.config.logger
            )

        return data


class GetConnectedAddonAuthParameter:

    @staticmethod
    def get_data_from_cache(cache_conn, key: str, **kwargs) -> dict:
        """
        It's overriding base class method ``get_data_from_cache``
        and fetch Addons data from the Cache database.
        It's using ``GetData`` class of ``caching`` package to perform this operation.
        """
        addons = cache_conn.get(
            operation_type=RedisOperationsTypeEnum.GET_JSON.value,
            payload={"key": key}
        )
        return addons

    @staticmethod
    def get_data_from_sql(db_session, logger=None, **kwargs):
        """
        This method is used to fetch data from the SQL database.
        It will fetch connected addon auth parameters from SQL
        """
        with SessionHandler(db_session) as db_conn:
            addons_data = get_connected_addon_parameters(
                conn=db_conn,
                connected_addon_auth_id=kwargs.get("connected_addon_auth_id")
            )
        if addons_data:
            return dict(addons_data.parameter)

        add_log(logger,
                "No Connected Addons auth parameters found in SQL database for Connected Addon "
                "{connected_addon_auth_id}".format(connected_addon_auth_id=kwargs.get("connected_addon_auth_id")))

    @staticmethod
    def get_data_from_elasticsearch(logger=None, **kwargs):
        """
        Its overriding base class method ``get_data_from_elasticsearch``.
        Here we don't require to fetch anything from the elastic search so
        it will return empty object
        """
        return {}

    @staticmethod
    def prepare_sync_payload(data, es_result, **kwargs):
        """
        This method will just return the data
        """
        return data


class ManageAddonAuthParameters:
    """ Manage Addon Auth Parameters """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_addon_auth_parameters(self, addon_version_id):
        """
        Get addon_auth parameters

        Required parameters:
            :param addon_version_id: Addon Version ID

        :return: Addon auth parameter object
        ---------------
        Example Object:
        ---------------
            {
               "keys":{
                  "scope":{"value":"https://www.googleapis.com/auth/calendar"}
               },
               "key_mapping":{
                  "code":"access_code",
                  "expires_in":"expires_in",
                  "access_token":"access_token",
                  "refresh_token":"refresh_token"
               },
               "refresh_token_property":{
                  "payload":{
                     "client_id":"{{client_id}}",
                     "grant_type":"{{grant_type_refresh_token}}",
                     "client_secret":"{{client_secret}}",
                     "refresh_token":"{{refresh_token}}"
                  },
                  "do_generate":true,
                  "requested_body_field":["access_token","expires_in"]
               },
               "request_token_property":{
                  "payload":{
                     "code":"{{access_code}}",
                     "client_id":"{{client_id}}",
                     "grant_type":"{{grant_type}}",
                     "redirect_uri":"{{redirect_uri}}",
                     "client_secret":"{{client_secret}}"
                  },
                  "requested_args":["code"],
                  "requested_body_field":["access_token", "refresh_token", "expires_in","token_type"]
               }
            }
        """
        key = RedisKeyEnum.ADDON_AUTH_PARAMETER.value.format(addon_version_id=addon_version_id)
        data = GetAddonAuthParameter.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger,
                    "Fetching data from SQL database for"
                    " Addon Auth Parameter {addon_version_id}".format(
                        addon_version_id=addon_version_id)
                    )
            data = SyncDataHandler.sync_data(
                self.config.db_session,
                self.config.cache_conn,
                GetAddonAuthParameter,
                key,
                addon_version_id=addon_version_id,
                logger=self.config.logger
            )

        return data


class GetAddonAuthParameter:

    @staticmethod
    def get_data_from_cache(cache_conn, key: str, **kwargs) -> dict:
        """
        It's overriding base class method ``get_data_from_cache``
        and fetch Addons data from the Cache database.
        It's using ``GetData`` class of ``caching`` package to perform this operation.
        """
        addons = cache_conn.get(
            operation_type=RedisOperationsTypeEnum.GET_JSON.value,
            payload={"key": key}
        )
        return addons

    @staticmethod
    def get_data_from_sql(db_session, logger=None, **kwargs):
        """
        This method is used to fetch data from the SQL database.
        It will fetch connected addon auth parameters from SQL
        """
        with SessionHandler(db_session) as db_conn:
            addons_data = get_addon_auth_parameters(
                conn=db_conn,
                addon_version_id=kwargs.get("addon_version_id")
            )
        if addons_data:
            return dict(addons_data.parameter)

        add_log(logger,
                "No Addons Auth Parameters found in SQL database for Add version "
                "{addon_version_id}".format(addon_version_id=kwargs.get("addon_version_id")))

    @staticmethod
    def get_data_from_elasticsearch(logger=None, **kwargs):
        """
        Its overriding base class method ``get_data_from_elasticsearch``.
        Here we don't require to fetch anything from the elastic search so
        it will return empty object
        """
        return {}

    @staticmethod
    def prepare_sync_payload(data, es_result, **kwargs):
        """
        This method will just return the data
        """
        return data


class ManageAddonFunctions:
    """ Manage Addon Auth Parameters """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_addon_functions(self, addon_version_id):
        """
        Get addon_auth functions

        Required parameters:
            :param addon_version_id: Addon Version ID

        :return: Addon functions

        """
        key = RedisKeyEnum.ADDON_FUNCTIONS.value.format(addon_version_id=addon_version_id)
        data = GetConnectedAddonAuthParameter.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger,
                    "Fetching data from SQL database for Connected"
                    " Addon Auth Parameter {addon_version_id}".format(
                        addon_version_id=addon_version_id)
                    )
            data = SyncDataHandler.sync_data(
                self.config.db_session,
                self.config.cache_conn,
                GetAddonFunctions,
                key,
                addon_version_id=addon_version_id,
                logger=self.config.logger
            )

        return data


class GetAddonFunctions:

    @staticmethod
    def get_data_from_cache(cache_conn, key: str, **kwargs) -> dict:
        """
        It's overriding base class method ``get_data_from_cache``
        and fetch Addons data from the Cache database.
        It's using ``GetData`` class of ``caching`` package to perform this operation.
        """
        addons = cache_conn.get(
            operation_type=RedisOperationsTypeEnum.GET_JSON.value,
            payload={"key": key}
        )
        return addons

    @staticmethod
    def get_data_from_sql(db_session, logger=None, **kwargs):
        """
        This method is used to fetch data from the SQL database.
        It will fetch connected addon auth parameters from SQL
        """
        with SessionHandler(db_session) as db_conn:
            addons_data = get_addon_functions(
                conn=db_conn,
                addon_version_id=kwargs.get("addon_version_id")
            )
        if addons_data:
            return addons_data

        add_log(logger,
                "No Addons Functions found in SQL database for Addon version "
                "{addon_version_id}".format(addon_version_id=kwargs.get("addon_version_id")))

    @staticmethod
    def get_data_from_elasticsearch(logger=None, **kwargs):
        """
        Its overriding base class method ``get_data_from_elasticsearch``.
        Here we don't require to fetch anything from the elastic search so
        it will return empty object
        """
        return {}

    @staticmethod
    def prepare_sync_payload(data, es_result, **kwargs):
        """
        This method will just return the data
        """
        result = dict()
        result['authentication_type'] = data[0].authentication_type
        result['functions'] = dict()
        for function in data:
            function = function
            result['functions'][function.function_name] = GetAddonFunctions.get_function_payload(function)
        return result

    @staticmethod
    def get_function_payload(data):
        return {
            "parameter": data.parameter,
            "script": data.script,
            "script_language": data.script_language
        }


class ManageConnectedAddonThirdPartyContactVariableMappings:
    """ Manage Connected Addon third party variable mappings """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_connected_addon_third_party_variable_mappings(self, connected_addon_auth_id):
        """
        Get connected-addon-connected_addon_third_party_variable_mappings

        Required parameters:
            :param connected_addon_auth_id: connected add on auth id

        :return: connected-addon-auth-id object
        ---------------
        Example Object:
        ---------------
            {
               "type":"active_campaign",
               "mappings":[
                  {
                     "variable":"abcd",
                     "is_overwrite":true,
                     "third_party_variable":"abc"
                  }
               ],
               "configs":{
                  "is_sync_enabled":false
               }
            }
        """
        key = RedisKeyEnum.CONNECTED_ADDON_THIRD_PARTY_VARIABLE_MAPPINGS.value.format(
            connected_addon_auth_id=connected_addon_auth_id)
        data = GetConnectedAddonAuthParameter.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger,
                    "Fetching data from SQL database for Connected"
                    " Addon {connected_addon_auth_id}".format(
                        connected_addon_auth_id=connected_addon_auth_id)
                    )
            data = SyncDataHandler.sync_data(
                self.config.db_session,
                self.config.cache_conn,
                GetConnectedAddonThirdPartyContactVariableMappings,
                key,
                connected_addon_auth_id=connected_addon_auth_id,
                logger=self.config.logger
            )

        return data


class GetConnectedAddonThirdPartyContactVariableMappings:

    @staticmethod
    def get_data_from_cache(cache_conn, key: str, **kwargs) -> dict:
        """
        It's overriding base class method ``get_data_from_cache``
        and fetch Addons data from the Cache database.
        It's using ``GetData`` class of ``caching`` package to perform this operation.
        """
        addons = cache_conn.get(
            operation_type=RedisOperationsTypeEnum.GET_JSON.value,
            payload={"key": key}
        )
        return addons

    @staticmethod
    def get_data_from_sql(db_session, logger=None, **kwargs):
        """
        This method is used to fetch data from the SQL database.
        It will fetch connected addon auth parameters from SQL
        """
        with SessionHandler(db_session) as db_conn:
            third_party_variable_mappings = get_connected_addon_third_party_variable_mapping(
                conn=db_conn,
                connected_addon_auth_id=kwargs.get("connected_addon_auth_id")
            )
        if third_party_variable_mappings:
            return third_party_variable_mappings

        add_log(logger,
                "No Connected Addons auth parameters found in SQL database for Connected Addon "
                "{connected_addon_auth_id}".format(connected_addon_auth_id=kwargs.get("connected_addon_auth_id")))

    @staticmethod
    def get_data_from_elasticsearch(logger=None, **kwargs):
        """
        Its overriding base class method ``get_data_from_elasticsearch``.
        Here we don't require to fetch anything from the elastic search so
        it will return empty object
        """
        return {}

    @staticmethod
    def prepare_sync_payload(data, es_result, **kwargs):
        """
        This method will just return the data
        """
        return {
            "type": data.type,
            "configs": data.configs,
            "mappings": data.mappings
        }


class ManageConnectedAddonGetDetailsByWebhookKey:
    """ Manage Connected Addon get details by webhook key """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_connected_addon_details_by_webhook_key(self, webhook_key):
        """
        Get connected addon details by webhook_key

        Required parameters:
            :param webhook_key: webhook_key

        :return: connected-addon-auth object

        """
        key = RedisKeyEnum.CONNECTED_ADDON_WEBHOOK_MAPPING.value.format(webhook_key=webhook_key)
        data = GetConnectedAddonAuthParameter.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger,
                    "Fetching data from SQL database for Connected"
                    " Addon Webhook {webhook_key}".format(webhook_key=webhook_key))
            data = SyncDataHandler.sync_data(
                self.config.db_session,
                self.config.cache_conn,
                GetConnectedAddonDetailsByWebhookKey,
                key,
                webhook_key=webhook_key,
                logger=self.config.logger
            )

        return data


class GetConnectedAddonDetailsByWebhookKey:

    @staticmethod
    def get_data_from_cache(cache_conn, key: str, **kwargs) -> dict:
        """
        It's overriding base class method ``get_data_from_cache``
        and fetch Addons data from the Cache database.
        It's using ``GetData`` class of ``caching`` package to perform this operation.
        """
        addons = cache_conn.get(
            operation_type=RedisOperationsTypeEnum.GET_JSON.value,
            payload={"key": key}
        )
        return addons

    @staticmethod
    def get_data_from_sql(db_session, logger=None, **kwargs):
        """
        This method is used to fetch data from the SQL database.
        It will fetch connected addon auth details from SQL
        """
        with SessionHandler(db_session) as db_conn:
            connected_addon = get_connected_addon_details_by_webhook_key(
                conn=db_conn,
                webhook_key=kwargs.get("webhook_key")
            )
        if connected_addon:
            return connected_addon

        add_log(logger,
                "No Connected Addons auth parameters found in SQL database for Connected Addon Webhook"
                "{webhook_key}".format(webhook_key=kwargs.get("webhook_key")))

    @staticmethod
    def get_data_from_elasticsearch(logger=None, **kwargs):
        """
        Its overriding base class method ``get_data_from_elasticsearch``.
        Here we don't require to fetch anything from the elastic search so
        it will return empty object
        """
        return {}

    @staticmethod
    def prepare_sync_payload(data, es_result, **kwargs):
        """
        This method will just return the data
        """
        return {
            "connected_addon_auth_id": data.connected_addon_auth_id,
            "mappings": data.mappings,
            "configs": data.configs,
            "account_id": data.account_id
        }

