import json
from DataAccessLib.common.utility import SingletonDecorator
from DataAccessLib.connection_network import ConnectionNetwork
from DataAccessLib.database.MySQL.channel import get_channels
from DataAccessLib.database.connect import SessionHandler
from DataAccessLib.handler import Getter


@SingletonDecorator
class ManageChannel:

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_channel(self):
        master_data = GetMasterChannel().get_channels_from_sql(self.config.db_session)
        parse_channels = {}
        for resource in master_data:
            if not resource.channel_name in parse_channels:
                provider = self.provider_payload(resource)
                parse_channels[resource.channel_name] = dict(
                    id=resource.channel_id,
                    priority=resource.priority,
                    name=resource.channel_name,
                    label=resource.channel_label,
                    is_coming_soon=not resource.channel_available, # using not for is_coming_soon field get false when channel is available
                    fields=resource.channel_fields if resource.channel_fields else [],
                    providers=[provider] if provider else []
                )
            else:
                provider = self.provider_payload(resource)
                parse_channels[resource.channel_name]['providers'].append(provider)
        response = []
        for channel, deatils in parse_channels.items():
            response.append(deatils)
        return response

    @staticmethod
    def provider_payload(resource):
        if resource.provider_name:
            provider = dict(
                id=resource.provider_id,
                name=resource.provider_name,
                label=resource.provider_name,
                is_coming_soon=not resource.provider_available, # using not for is_coming_soon field get false when channel is available
                fields=resource.provider_fields if resource.provider_fields else []
            )
            return provider


class GetMasterChannel(Getter):

    @staticmethod
    def get_channels_from_sql(db_session):
        with SessionHandler(db_session) as db_conn:
            result = get_channels(db_conn)
        if result:
            return result
        return []
