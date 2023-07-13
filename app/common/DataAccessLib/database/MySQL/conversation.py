from sqlalchemy import func

from DataAccessLib.database.models import (Conversation, Bot)


def get_conversation_count_between_date_range(conn, start_at, end_at, bots):
    """
    SQLAlchemy query to get conversation count between given durations
    Required parameters:

       :param conn: <<Class object>>: SQL connection object
       :param start_at: DATE: subscription current billing cycle start date
       :param end_at: DATE: subscription current billing cycle end date
       :param bots: LIST: list of bots of the account
       :return: conversation count
    """
    return conn.query(Conversation).with_entities(
        func.count(Conversation.id).label("count")
    ).filter(func.DATE(Conversation.session_start_at).between(start_at, end_at),
             Conversation.bot_id.in_(bots),
             Conversation.channel != "PREV_WEB").one()


def get_account_total_conversation_count(conn, account_id):
    """
    SQLAlchemy query to get account total conversation count
    Required parameters:
       :param conn: <<Class object>>: SQL connection object
       :param account_id: Account Unique ID
       :return: conversation count
    """
    return conn.query(Conversation).with_entities(
        func.count(Conversation.id).label("count")
    ).join(
        Bot, Bot.id == Conversation.bot_id
    ).filter(Bot.account_id == account_id).first()
