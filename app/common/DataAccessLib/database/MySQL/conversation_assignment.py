from UtilsLib import (ConversationStatusEnum)
from sqlalchemy import func, and_

from DataAccessLib.database.models import (Conversation)


def get_user_workload_by_account_id(conn, bots, users):
    """
    SQLAlchemy query to fetch the user workload from SQL database.

    Required parameters:
       :param conn: <<Class object>>: SQL connection object
       :param bots: TUPLE: bot list of the account
       :param users: TUPLE: user list of the account

    :return: Workload of the users
   """

    return conn.query(Conversation).with_entities(
        Conversation.assigned_to,
        func.group_concat(Conversation.id),
    ).filter(and_(
        Conversation.conversation_status == ConversationStatusEnum.OPEN.value,
        Conversation.bot_id.in_(bots),
        Conversation.assigned_to.in_(users))
    ).order_by(
        func.max(Conversation.assignee_modified_at)
    ).group_by(
        Conversation.assigned_to
    ).all()
