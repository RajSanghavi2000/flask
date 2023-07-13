from DataAccessLib.database.models import (User, Bot, UserRole, UserSettings, AppNotificationToken)
from sqlalchemy import and_


def get_agent_details(conn, agent_id):
    """
    SQLAlchemy query to fetch the Agent data from SQL database.

    Required parameters:
       :param conn: <<Class object>>: SQL connection object
       :param agent_id: INTEGER: Unique agent id

    :return: Agent Data
   """

    return conn.query(User).with_entities(
        User.id,
        User.email,
        User.first_name,
        User.last_name,
        User.image_name,
        User.user_type_master_id
    ).filter(User.id == agent_id).first()


def get_agent_roles(conn, agent_id):
    """
    SQLAlchemy query to fetch the Agent data from SQL database.

    Required parameters:
       :param conn: <<Class object>>: SQL connection object
       :param agent_id: INTEGER: Unique agent id

    :return: Agent roles
   """
    return conn.query(Bot).with_entities(
        Bot.account_id.label("account_id"),
        Bot.id.label("bot_id"),
        UserRole.user_role_master_id.label('user_role_master_id')
    ).join(
        UserRole, Bot.account_id == UserRole.account_id
    ).filter(UserRole.user_id == agent_id).all()


def get_agent_status(conn, agent_id):
    """
    SQLAlchemy query to fetch the Agent data from SQL database.

    Required parameters:
       :param conn: <<Class object>>: SQL connection object
       :param agent_id: INTEGER: Unique agent id

    :return: Agent status
   """

    return conn.query(UserSettings).with_entities(
        UserSettings.user_status_master_id.label("user_status_master_id"),
    ).filter(UserSettings.user_id == agent_id).first()


def get_multiple_agent_details(conn, agent_ids):
    """
    SQLAlchemy query to fetch the Agent data from SQL database.

    Required parameters:
       :param conn: <<Class object>>: SQL connection object
       :param agent_ids: List: Unique agent id list

    :return: Agent Data
   """

    return conn.query(User).with_entities(
        User.id,
        User.email,
        User.first_name,
        User.last_name,
        User.image_name,
        User.user_type_master_id
    ).filter(User.id.in_(tuple(agent_ids))).all()


def get_user_preferences(conn, user_id):
    """
    SQLAlchemy query to fetch the Agent data from SQL database.

    Required parameters:
       :param conn: <<Class object>>: SQL connection object
       :param user_id: INTEGER: Unique user id

    :return: User Preferences
   """

    return conn.query(UserSettings).with_entities(
        UserSettings.preferences.label("preferences"),
    ).filter(UserSettings.user_id == user_id).first()


def get_user_notification_preferences(conn, user_ids):
    """
    SQLAlchemy query to fetch the Agent notification preferences from SQL database.

    Required parameters:
       :param conn: <<Class object>>: SQL connection object
       :param user_ids: LIST<INTEGER>: Unique user id list

    :return: User Preferences
   """

    return conn.query(UserSettings).with_entities(
        UserSettings.notification_events,
        UserSettings.user_id,
    ).filter(UserSettings.user_id.in_(tuple(user_ids))).all()


def get_user_notification_tokens(conn, user_ids, _type):
    """
    SQLAlchemy query to fetch the Agent notification tokens from SQL database.

    Required parameters:
       :param conn: <<Class object>>: SQL connection object
       :param user_ids: LIST<INTEGER>: Unique user id list
       :param _type: PWA or react-native

    :return: User Preferences
   """

    return conn.query(UserSettings).with_entities(
        AppNotificationToken.token,
    ).filter(and_(AppNotificationToken.user_id.in_(tuple(user_ids)),
             AppNotificationToken.type == _type)).all()
