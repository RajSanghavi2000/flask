from sqlalchemy import func
from DataAccessLib.database.models import (OutboundMessageBalanceAudit)


def get_multiple_account_outbound_message_latest_audit(conn, account_ids, date):
    """
    SQLAlchemy query to get subscription outbound message latest audit
    Required parameters:

       :param conn: <<Class object>>: SQL connection object
       :param account_ids: LIST: account ids
       :param date: DATE: date
       :return: subscription outbound message latest audit
    """
    return conn.query(OutboundMessageBalanceAudit).with_entities(
        OutboundMessageBalanceAudit.outbound_message_balance,
        OutboundMessageBalanceAudit.outbound_message_remaining_balance,
        OutboundMessageBalanceAudit.account_id,
        OutboundMessageBalanceAudit.plan_id,
        OutboundMessageBalanceAudit.id,
        OutboundMessageBalanceAudit.start_at,
        OutboundMessageBalanceAudit.end_at,
    ).filter(OutboundMessageBalanceAudit.account_id.in_(tuple(account_ids)),
             func.DATE(date).between(OutboundMessageBalanceAudit.start_at, OutboundMessageBalanceAudit.end_at))\
        .order_by(OutboundMessageBalanceAudit.id).all()

