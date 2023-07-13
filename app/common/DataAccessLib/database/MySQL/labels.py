from DataAccessLib.database.models import (ConversationLabel)


def get_account_labels(conn, account_id):
    """
    SQLAlchemy query to fetch the Dialog <-> Feature mapping data from SQL database.

    Required parameters:
       :param conn: <<Class object>>: SQL connection object
       :param account_id: INTEGER: Unique account id

    :return: Dialog <-> Feature mapping data
   """
    return conn.query(ConversationLabel).with_entities(
        ConversationLabel.id,
        ConversationLabel.label,
        ConversationLabel.created_by,
        ConversationLabel.created_at
    ).filter(ConversationLabel.account_id == account_id).order_by(ConversationLabel.id).all()

