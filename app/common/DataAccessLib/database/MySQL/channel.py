from sqlalchemy import and_

from DataAccessLib.database.models import (Channel, ChannelProvider)


def get_channels(conn):
    return conn.query(Channel).with_entities(
        Channel.id.label('channel_id'),
        Channel.name.label('channel_name'),
        Channel.label.label('channel_label'),
        Channel.fields.label('channel_fields'),
        Channel.is_available.label('channel_available'),
        Channel.priority,
        ChannelProvider.id.label('provider_id'),
        ChannelProvider.name.label('provider_name'),
        ChannelProvider.channel_id.label('channel_provider_channel_id'),
        ChannelProvider.is_available.label('provider_available'),
        ChannelProvider.fields.label('provider_fields')
    ).outerjoin(ChannelProvider, and_(ChannelProvider.channel_id == Channel.id, ChannelProvider.is_available == 1)
                ).filter(and_(Channel.is_visible == 1)).order_by(
        Channel.priority.asc(), ChannelProvider.id.asc()).all()
