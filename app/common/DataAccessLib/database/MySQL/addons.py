from sqlalchemy import and_, func
from DataAccessLib.database.models import (
    AddonVersion, ConnectedAddon, CodeBlock,
    ScriptLanguage, AddonAuth, ConnectedAddonAuth,
    AuthenticationType, ThirdPartyVariableMappings
)


def get_addons_data(conn, redis_key):
    """ Connect to MySQL DB and fetch addons_data

    get single addons_data using redis_key
    # ToDo: Add ORM Query to Get Addons Data
    @param conn:
    @param redis_key:
    @return: addons_data
    """
    return conn.query(ConnectedAddon).with_entities(
        ConnectedAddon.id.label('connected_addon_id'),
        ConnectedAddon.addon_version_id,
        ConnectedAddon.bot_lead_id,
        ConnectedAddon.redis_key,
        AddonAuth.parameter.label('addon_auth_parameter'),
        ConnectedAddonAuth.parameter.label('auth_parameter'),
        CodeBlock.function_name,
        CodeBlock.script,
        CodeBlock.parameter,
        ScriptLanguage.name.label('script_language')
    ).outerjoin(
        ConnectedAddonAuth, ConnectedAddon.id == ConnectedAddonAuth.connected_addon_id
    ).join(
        AddonVersion, ConnectedAddon.addon_version_id == AddonVersion.id
    ).join(
        CodeBlock, AddonVersion.id == CodeBlock.addon_version_id
    ).join(
        AddonAuth, AddonVersion.id == AddonAuth.addon_version_id
    ).join(
        ScriptLanguage, CodeBlock.script_language_id == ScriptLanguage.id
    ).filter(
        ConnectedAddon.redis_key == redis_key
    ).order_by(
        ConnectedAddon.redis_key
    ).all()


def get_addon_version_id_and_connected_addon_auth_id(conn, function_name, account_id):
    """
    Get addon-version-id and connected-addon-auth-id as per the function name and account-id.
    @param conn: database connection
    @param function_name: code-block function name
    @param account_id: account-id
    @return: addon-version-id and connected-addon-auth-id
    """

    return conn.query(AddonVersion).with_entities(
        AddonVersion.id.label('addon_version_id'),
        ConnectedAddonAuth.id.label('connected_addon_auth_id'),
    ).join(
        CodeBlock, AddonVersion.id == CodeBlock.addon_version_id
    ).join(
        ConnectedAddon, AddonVersion.id == ConnectedAddon.addon_version_id
    ).outerjoin(
        ConnectedAddonAuth, ConnectedAddon.id == ConnectedAddonAuth.connected_addon_id
    ).filter(
        and_(
            CodeBlock.function_name == function_name,
            ConnectedAddon.account_id == account_id
        )
    ).order_by(
        ConnectedAddonAuth.id
    ).first()


def get_addon_version_id_for_the_function_name(conn, function_name):
    """
    Get addon-version-id as per the function name.
    @param conn: database connection
    @param function_name: code-block function name
    @return: addon-version-id
    """

    return conn.query(CodeBlock).with_entities(
        CodeBlock.addon_version_id
    ).filter(
            CodeBlock.function_name == function_name
    ).first()


def get_connected_addon_parameters(conn, connected_addon_auth_id):
    """
    Get connected_addon_auth_id parameters from SQL
    @param conn: database connection
    @param connected_addon_auth_id: connected_addon_auth_id
    @return: connected addon ID parameters
    """

    return conn.query(ConnectedAddonAuth).with_entities(
        ConnectedAddonAuth.parameter.label('parameter')
    ).filter(
        ConnectedAddonAuth.id == connected_addon_auth_id
    ).first()


def get_addon_auth_parameters(conn, addon_version_id):
    """
    Get addon_auth_id parameters from SQL
    @param conn: database connection
    @param addon_version_id: Add on version ID
    @return: Addon Auth parameters
    """

    return conn.query(AddonAuth).with_entities(
        AddonAuth.parameter
    ).filter(
        AddonAuth.addon_version_id == addon_version_id
    ).first()


def get_addon_functions(conn, addon_version_id):
    """
    Get addon functions
    @param conn: database connection
    @param addon_version_id: Add on version ID
    @return: Addon functions object
    """
    return conn.query(CodeBlock).with_entities(
        CodeBlock.function_name.label('function_name'),
        CodeBlock.parameter.label('parameter'),
        CodeBlock.script.label('script'),
        ScriptLanguage.name.label('script_language'),
        AuthenticationType.key.label('authentication_type')
    ).join(
        AddonAuth, AddonAuth.addon_version_id == CodeBlock.addon_version_id
    ).join(
        AuthenticationType, AuthenticationType.id == AddonAuth.authentication_type_id
    ).join(
        ScriptLanguage, ScriptLanguage.id == CodeBlock.script_language_id
    ).filter(
        CodeBlock.addon_version_id == addon_version_id
    ).all()


def get_connected_addon_third_party_variable_mapping(conn, connected_addon_auth_id):
    """
    Get connected_addon_auth_id third party variable mapping from SQL
    @param conn: database connection
    @param connected_addon_auth_id: connected_addon_auth_id
    @return: connected addon ID parameters
    """

    return conn.query(ThirdPartyVariableMappings).with_entities(
        ThirdPartyVariableMappings.mappings,
        ThirdPartyVariableMappings.configs,
        ThirdPartyVariableMappings.type
    ).filter(
        ThirdPartyVariableMappings.connected_addon_auth_id == connected_addon_auth_id
    ).first()


def get_connected_addon_details_by_webhook_key(conn, webhook_key):
    """
    @param conn: database connection
    @param webhook_key: webhook_key
    @return: connected addon Details
    """

    return conn.query(ConnectedAddonAuth).with_entities(
        ConnectedAddonAuth.id.label("connected_addon_auth_id"),
        ThirdPartyVariableMappings.mappings,
        ThirdPartyVariableMappings.configs,
        ConnectedAddon.account_id
    ).join(
        ConnectedAddon, ConnectedAddon.id == ConnectedAddonAuth.connected_addon_id
    ).join(
        ThirdPartyVariableMappings, ConnectedAddonAuth.id == ThirdPartyVariableMappings.connected_addon_auth_id
    ).filter(
        func.json_extract(ConnectedAddonAuth.parameter, '$.keys.webhook_key.value') == webhook_key
    ).first()
