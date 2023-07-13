from DataAccessLib.database.models import (ChannelConfiguration, Channel, ChannelProvider)


def get_channel_configuration(conn, channel_configuration_id):
    """
    SQLAlchemy query to get channel configurations details
    Required parameters:

       :param conn: <<Class object>>: SQL connection object
       :param channel_configuration_id: INTEGER: channel configuration id
       :return: channel configurations
    """
    return conn.query(ChannelConfiguration).with_entities(
        ChannelConfiguration.id,
        ChannelConfiguration.key,
        ChannelConfiguration.account_id,
        ChannelConfiguration.channel_id,
        ChannelConfiguration.channel_provider_id,
        ChannelConfiguration.config_identity,
        ChannelConfiguration.configuration,
    ).filter(ChannelConfiguration.id == channel_configuration_id).first()


def get_channel_account_configurations(conn, account_id, channel_id):
    return conn.query(ChannelConfiguration).with_entities(
        ChannelConfiguration.id,
        ChannelConfiguration.channel_id,
        ChannelConfiguration.channel_provider_id,
        ChannelConfiguration.key,
        Channel.name.label('channel'),
        ChannelProvider.name.label('provider'),
        ChannelConfiguration.config_identity,
        ChannelConfiguration.configuration,
    ).outerjoin(
        ChannelProvider, ChannelProvider.id == ChannelConfiguration.channel_provider_id
    ).join(
        Channel, Channel.id == ChannelConfiguration.channel_id
    ).filter(ChannelConfiguration.account_id == account_id, ChannelConfiguration.channel_id == channel_id).order_by(
        ChannelConfiguration.created_at).all()
