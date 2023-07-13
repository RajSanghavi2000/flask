from DataAccessLib.database.models import (ChannelConfiguration,
                                           FacebookPages,
                                           Bot,
                                           VoiceWebChannelConfiguration,
                                           Preferences)

from sqlalchemy import and_


def get_messenger_channel_bot_id(conn, page_id):
    """
    SQLAlchemy query to get bot id by Facebook page id
    Required parameters:

       :param conn: <<Class object>>: SQL connection object
       :param page_id: STRING: Unique page id
       :return: bot id
    """
    return conn.query(ChannelConfiguration).with_entities(
        ChannelConfiguration.bot_lead_id.label("bot_id")
    ).join(
        FacebookPages, FacebookPages.channel_configuration_id == ChannelConfiguration.id
    ).filter(FacebookPages.page_id == page_id).first()


def get_web_channel_bot_id(conn, publish_key):
    """
    SQLAlchemy query to get bot id by Web publish key
    Required parameters:

       :param conn: <<Class object>>: SQL connection object
       :param publish_key: STRING: Unique bot publish key
       :return: bot id
    """
    return conn.query(Bot).with_entities(
        Bot.id.label("bot_id")
    ).filter(Bot.publish_key == publish_key).first()


def get_voiceweb_channel_bot_id(conn, webhook_key):
    """
    SQLAlchemy query to get bot id by VoiceWeb webhook kwy
    Required parameters:

       :param conn: <<Class object>>: SQL connection object
       :param webhook_key: STRING: Unique webhook_key
       :return: bot id
    """
    return conn.query(ChannelConfiguration).with_entities(
        ChannelConfiguration.bot_lead_id.label("bot_id")
    ).join(
        VoiceWebChannelConfiguration, VoiceWebChannelConfiguration.channel_configuration_id == ChannelConfiguration.id
    ).filter(VoiceWebChannelConfiguration.webhook_key == webhook_key).first()


def get_configured_bots(conn, channel_configurations_key):
    """
    SQLAlchemy query to get bots by channel configurations key
    Required parameters:
       :param conn: <<Class object>>: SQL connection object
       :param channel_configurations_key: STRING: Unique channel configurations key
       :return: bots
    """
    return conn.query(Preferences).with_entities(
        Preferences.bot_lead_id.label('bot_id'),
        Bot.account_id,
        ChannelConfiguration.config_identity
    ).join(
        Bot, Bot.id == Preferences.bot_lead_id
    ).join(
        ChannelConfiguration, and_(ChannelConfiguration.account_id == Bot.account_id,
                                   Preferences.channel_configuration_id == ChannelConfiguration.id)
    ).filter(and_(ChannelConfiguration.key == channel_configurations_key, Bot.is_deleted == 0,
                  Bot.is_active == 1)).order_by(Bot.created_at).all()


def get_attached_channel_configuration_key_by_bot_ids(conn, bot_ids):
    """
    SQLAlchemy query to get channel configurations keys by bot IDs
    Required parameters:
       :param conn: <<Class object>>: SQL connection object
       :param bot_ids: LIST: Unique bot ids
       :return: bots
    """
    return conn.query(ChannelConfiguration).with_entities(
        ChannelConfiguration.key
    ).join(
        Preferences,  Preferences.channel_configuration_id == ChannelConfiguration.id
    ).filter(Preferences.bot_lead_id.in_(tuple(bot_ids))).all()
