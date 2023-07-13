from DataAccessLib.database.models import (Variable)


def get_variable(conn, account_id):
    """
    SQLAlchemy query to get format of the variable
    Required parameters:

       :param conn: <<Class object>>: SQL connection object
       :param account_id: INTEGER: Unique account id
    :return: Preview redis key
    """
    return conn.query(Variable).with_entities(
        Variable.format,
        Variable.status,
        Variable.error_message,
        Variable.parameter,
        Variable.validation,
        Variable.normalized_parameter,
        Variable.is_contact_page_qualified_variable,
        Variable.type,
        Variable.name
    ).filter(
        Variable.account_id == account_id
    ).all()
