from sqlalchemy import func

from DataAccessLib.database.models import (User, Bot, Account, Version, Preferences,
                                           ChannelConfiguration, SpreadSheet, Faq,
                                           FacebookPages, FlowDiagram)


def get_bot_details(conn, bot_id):
    """
    SQLAlchemy query to fetch the Bot data from SQL database.

    Required parameters:
       :param conn: <<Class object>>: SQL connection object
       :param bot_id: INTEGER: Unique bot id

    :return: Bot Data
   """
    return conn.query(Bot).with_entities(
        func.distinct(Bot.id).label("bot_id"), Bot.preview_key.label("preview_key"),
        Account.status.label("account_status"), Account.key.label("account_key"),
        Account.id.label("account_id"),
        User.id.label("created_by"),
        User.first_name.label("user_first_name"),
        User.last_name.label("user_last_name"),
        Version.id.label("version_id"),
        Bot.publish_key.label("publish_key"), Bot.preview_version_id.label("preview_version_id"),
        Bot.is_active.label("is_active"),
        Bot.bot_name.label('bot_title'),
        Bot.created_at,
        Bot.type,
        Bot.is_deleted.label("is_deleted"),
        Bot.campaign_details.label("campaign_details"),
        ChannelConfiguration.channel_id.label("channel_id"),
        Preferences.language.label("language"),
        Preferences.outbound_type,
        Preferences.channel_configuration_id,
        SpreadSheet.response_sheet_id.label("response_spreadsheet_id"),
        SpreadSheet.id.label("spreadsheet_id"),
        SpreadSheet.sheet_id,
        Preferences.trigger_variables
    ).outerjoin(
        Preferences, Bot.id == Preferences.bot_lead_id
    ).outerjoin(
        User, Bot.created_by == User.id
    ).join(
        Account, Bot.account_id == Account.id
    ).join(
        Version, Bot.version_id == Version.id
    ).outerjoin(
        ChannelConfiguration, Bot.id == ChannelConfiguration.bot_lead_id
    ).outerjoin(
        SpreadSheet, Version.spreadsheet_id == SpreadSheet.id
    ).filter(Bot.id == bot_id,
             ).order_by(Bot.id.desc()).limit(1).first()


def get_messenger_channel_configurations(conn, bot_id):
    """
    SQLAlchemy query to get messenger channel configurations
    Required parameters:

       :param conn: <<Class object>>: SQL connection object
       :param bot_id: INTEGER: bot id
       :return: channel configurations
    """
    return conn.query(FacebookPages).with_entities(
        FacebookPages.page_access_token.label("page_access_token"),
        FacebookPages.page_id.label("page_id")
    ).join(
        ChannelConfiguration, ChannelConfiguration.id == FacebookPages.channel_configuration_id
    ).filter(ChannelConfiguration.bot_lead_id == bot_id).first()


def get_bot_conversation_dialog(conn, version_id):
    """
    SQLAlchemy query to get Bot conversation dialog data
    Required parameters:

       :param conn: <<Class object>>: SQL connection object
       :param version_id: INTEGER: version id
       :return: bot conversation dialog
    """
    return conn.query(Version).with_entities(
        Version.conversation_dialog.label("conversation_dialog"),
    ).filter(Version.id == version_id).first()


def get_multiple_bot_trigger_rules(conn, bot_ids):
    """
    SQLAlchemy query to fetch the bot trigger rules
    Required parameters:

       :param conn: <<Class object>>: SQL connection object
       :param bot_ids: LIST<INTEGER>: Unique bot id list
    :return: List of bot referral urls
    """
    return conn.query(Preferences).with_entities(
        Preferences.bot_lead_id.label("bot_id"),
        Preferences.trigger_rules
    ).filter(Preferences.bot_lead_id.in_(tuple(bot_ids))).all()


def get_bot_version_from_sql(conn, bot_id):
    """
    Get bot version from SQL

    Required parameters:

       :param conn: <<Class object>>: SQL connection object
       :param bot_id: <INTEGER>: Unique id assigned to every bot
    :return: bot versions
    """

    return conn.query(Version).with_entities(
        func.distinct(Version.id).label("version_id")
    ).join(
        FlowDiagram, FlowDiagram.version_id == Version.id
    ).join(
        Bot, Bot.id == FlowDiagram.bot_id
    ).filter(Bot.id == bot_id, Version.is_deployed == 1, Bot.is_deleted == 0).all()


def fetch_bot_id_by_publish_key(conn, publish_key):
    """
    SQLAlchemy query to fetch bot_lead_id
    Required parameters:

       :param conn: <<Class object>>: SQL connection object
       :param publish_key: STRING
    :return: bot_lead_id
    """
    bot_lead_id = conn.query(Bot).with_entities(Bot.id).filter(Bot.publish_key == publish_key).first()
    return bot_lead_id[0] if bot_lead_id else None
