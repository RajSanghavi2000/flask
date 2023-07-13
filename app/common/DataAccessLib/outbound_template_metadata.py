from DataAccessLib.connection_network import ConnectionNetwork
from DataAccessLib.database.connect import SessionHandler
from DataAccessLib.database.MySQL.outbound_templates_metadata import get_outbound_template_metadata
from DataAccessLib.handler import Getter


class GetOutboundTemplateMetadata:

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_outbound_template_metadata(self):
        response = GetData().get_outbound_template_metadata_from_db(self.config.db_session)
        return {
            "whatsapp_providers": [
                {
                    "name": item.name,
                    "categories": item.categories,
                    "languages": item.languages
                }
                for item in response
            ]
        }


class GetData(Getter):

    @staticmethod
    def get_outbound_template_metadata_from_db(db_session):
        with SessionHandler(db_session) as db_conn:
            result = get_outbound_template_metadata(db_conn)
            return result or []
