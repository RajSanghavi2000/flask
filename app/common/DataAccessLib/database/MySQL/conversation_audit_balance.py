from DataAccessLib.database.models import (ConversationBalanceAudit)


def get_subscription_start_at_and_end_at(conn, account_id):
    """
    SQLAlchemy query to get subscription start_at & end_at
    Required parameters:

       :param conn: <<Class object>>: SQL connection object
       :param account_id: INTEGER: account id
       :return: subscription current billing cycle start_at & end_at
    """
    return conn.query(ConversationBalanceAudit).with_entities(
        ConversationBalanceAudit.start_at,
        ConversationBalanceAudit.end_at,
    ).filter(ConversationBalanceAudit.account_id == account_id,
             ConversationBalanceAudit.type == "Monthly").order_by(ConversationBalanceAudit.id.desc()).first()

