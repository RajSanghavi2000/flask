from DataAccessLib.database.models import ChannelProvider


def get_twilio_managed_auth(conn, provider):
    """
    SQLAlchemy query to get conversation count between given durations
    Required parameters:

       :param conn: <<Class object>>: SQL connection object
       :param provider: STRING: Provider name
       :return: provider auth
    """
    return conn.query(ChannelProvider).with_entities(
        ChannelProvider.auth
    ).filter(ChannelProvider.name == provider).one()
