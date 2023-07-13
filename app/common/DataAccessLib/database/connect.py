import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..common.DataAccessLib.connection_network import ConnectionNetwork
from DataAccessLib.common import get_database_url, get_database, DatabaseEnum


def get_database_connector(**kwargs):
    """
    This method is used to configure ORM. Here it's using SQLAlchemy ORM and will use it's ``create_engine`` method
    to create DB engine and ``sessionmaker`` to create DB Session.
    - DB Session use to create new DB connections

    Optional kwargs parameters:
        :param sql_database: STRING:SQL database that you want to configure. Default it's MySQL.
        :param cache_conn: <<Class object>>: Cache connection object
        :param logger: <<Class object>>: Logger object

    :return: DB <<Class engine>> and <<Class Session>>

    Step to configure orm:
        Step 1: from DataAccessLib.database.config import configure_orm
        Step 2: Use ``configure_orm`` method with required parameters

    Example:
        from DataAccessLib.database.config import configure_orm

        engine, Session = configure_orm(sql_database="MySQL")
    """
    database = get_database(kwargs.get("sql_database"))
    credentials = get_credentials(database)
    url = get_database_url(database).format(user=credentials.get("user"),
                                            password=credentials.get("password"),
                                            host=credentials.get("host"),
                                            database=credentials.get("database"))
    engine = create_engine(url, pool_recycle=int(credentials.get("pool_recycle")),
                           pool_size=int(credentials.get("pool_size")),
                           max_overflow=int(credentials.get("max_overflow")), echo=False)

    Session = sessionmaker(bind=engine)

    ConnectionNetwork(db_session=Session, cache_conn=kwargs.get("cache_conn"), logger=kwargs.get("logger"))

    return engine, Session


def get_credentials(database):
    """
    Required os parameters:
        MySQL:
            :param MYSQL_DATABASE_USER: STRING: User name of MySQL database.
            :param MYSQL_DATABASE_PASSWORD: STRING: Password of MySQL database.
            :param MYSQL_DATABASE_HOST: STRING:Address of MySQL database server
            :param MYSQL_DATABASE_DB: STRING: Database name that MySQL want to use
            :param MYSQL_DATABASE_CONNECTION_POOL_SIZE: INTEGER: MySQL database connection pool size
            :param MYSQL_DATABASE_CONNECTION_POOL_MAX_OVERFLOW_SIZE: INTEGER: MySQL database max connection pool size
            :param MYSQL_DATABASE_CONNECTION_POOL_RECYCLE: INTEGER: MySQL database connection recycle time

    :param database: STRING: SQL database
    :return: Credential JSON
    """

    if database == DatabaseEnum.MYSQL.value:
        return {"user": os.environ.get("MYSQL_DATABASE_USER"),
                "password": os.environ.get("MYSQL_DATABASE_PASSWORD"),
                "host": os.environ.get("MYSQL_DATABASE_HOST"),
                "database": os.environ.get("MYSQL_DATABASE_DB"),
                "pool_size": os.environ.get("MYSQL_DATABASE_CONNECTION_POOL_SIZE"),
                "max_overflow": os.environ.get("MYSQL_DATABASE_CONNECTION_POOL_MAX_OVERFLOW_SIZE"),
                "pool_recycle": os.environ.get("MYSQL_DATABASE_CONNECTION_POOL_RECYCLE")
                }


class SessionHandler(object):
    """
    This class is use to handle the DB connection. This class can be use with ``with`` statement.
    - At the starting of the ``with`` statement it will invoke ``__enter__`` method to create the connection
    - At the end of the ``with`` statement it will invoke ``__exit__`` method to close the connection

    Steps to use:
        Step 1: Configure ORM
        Step 2: from DataAccessLib.database.connect import SessionHandler
        Step 3: Use ``SessionHandler`` with ``with`` statement to create the connection

    Example:
        from DataAccessLib.database.config import configure_orm

        engine, Session = configure_orm(SQL_DATABASE_USER="Your SQL database user",
                         SQL_DATABASE_PASSWORD="Your SQL database password",
                         SQL_DATABASE_HOST="Your SQL database host",
                         SQL_DATABASE_DB="Your SQL database DB",
                         SQL_DATABASE_CONNECTION_POOL_SIZE="SQL database pool connection size",
                         SQL_DATABASE_CONNECTION_POOL_MAX_OVERFLOW_SIZE="SQL database max connection pool size")

    """

    def __init__(self, session_maker):
        self.session = None
        self.session_maker = session_maker

    def __enter__(self):
        """It's invoking ``connect`` method to create the connection"""
        self.session = connect(self.session_maker)
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        """It invoking ``close`` method to close the connection"""
        close(self.session)


def connect(session_maker):
    """Create DB connection object"""
    return session_maker()


def close(session):
    if session is not None:
        """Close DB connection"""
        session.close()

