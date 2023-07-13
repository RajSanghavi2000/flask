from DataAccessLib.database.models import (Plan)


def get_plans_by_economical_priority(conn):
    """
    SQLAlchemy query to fetch <-> plan by economical priority from SQL database.

    Required parameters:
       :param conn: <<Class object>>: SQL connection object

    :return: plans with economical priority
   """
    return conn.query(Plan).with_entities(
        Plan.id.label("plan_id")
    ).filter(
        Plan.economical_priority.isnot(None)
    ).order_by(Plan.economical_priority.desc()).all()
