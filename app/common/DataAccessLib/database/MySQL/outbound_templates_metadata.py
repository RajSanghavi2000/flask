from DataAccessLib.database.models import OutboundTemplateMetadata, ChannelProvider


def get_outbound_template_metadata(conn):
    """
    SQLAlchemy Query to get outbound templates metadata.
    Required parameters:

       :param conn: <<Class object>>: SQL connection object
       :return: List containing provider name, template categories, languages
    """
    return conn.query(OutboundTemplateMetadata).join(ChannelProvider).filter(OutboundTemplateMetadata.channel_provider_id == ChannelProvider.id).with_entities(
        ChannelProvider.name,
        OutboundTemplateMetadata.categories,
        OutboundTemplateMetadata.languages
    ).all()
