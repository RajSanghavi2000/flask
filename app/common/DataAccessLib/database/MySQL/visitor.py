from sqlalchemy import func, or_, case, and_
from DataAccessLib.database.models import Conversation, Visitor, VisitorExternalKeyMapping, Bot


def get_visitor_key_using_external_key(conn, external_key):
    """This method is sued to get visitor key from the visitor_key_external_key mapping SQL table using external_key"""

    return conn.query(Visitor).with_entities(
        Visitor.key.label("visitor_key")
    ).join(
        VisitorExternalKeyMapping, Visitor.id == VisitorExternalKeyMapping.visitor_id
    ).filter(VisitorExternalKeyMapping.external_key == external_key).first()


def get_visitor_from_sql(conn, visitor_key):
    """This method is used to get visitor object from the SQL database. We can have multiple active conversations
        for the single visitor so we will get rows from the SQL"""

    return conn.query(Visitor).with_entities(
        Visitor.id.label('id'), VisitorExternalKeyMapping.external_key.label('external_key'), Visitor.key.label('key'),
        Visitor.account_id.label('account_id'), VisitorExternalKeyMapping.channel_id.label('channel_id')
    ).join(
        VisitorExternalKeyMapping, Visitor.id == VisitorExternalKeyMapping.visitor_id
    ).filter(Visitor.key == visitor_key).all()


def get_visitor_default_name_counter_and_series(conn, account_id):
    """This method is used to get visitor default name counter and series object from the SQL database"""

    return conn.query(Conversation).with_entities(func.count(func.distinct(
        Conversation.visitor_id)).label("count")
    ).join(
        Bot, Conversation.bot_id == Bot.id
    ).filter(Bot.account_id == account_id).first()
