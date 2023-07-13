from DataAccessLib.database.models import (OutBoundTemplate, OutboundTemplateMediaMapping)


def get_outbound_templates(conn, template_id):
    """ SQLAlchemy query to get team members of the team

    Required parameters:
       :param conn: <<Class object>>: SQL connection object
       :param template_id: INTEGER: Unique account id
    :return: Template Details
    """
    return conn.query(OutBoundTemplate).with_entities(
        OutBoundTemplate.id.label('template_id'),
        OutBoundTemplate.name,
        OutBoundTemplate.channel_id,
        OutBoundTemplate.channel_provider_id,
        OutBoundTemplate.channel_configuration_id,
        OutBoundTemplate.category,
        OutBoundTemplate.status,
        OutBoundTemplate.components,
        OutBoundTemplate.configurations,
        OutboundTemplateMediaMapping.media_id
    ).outerjoin(OutboundTemplateMediaMapping, OutBoundTemplate.id == OutboundTemplateMediaMapping.template_id).filter(
        OutBoundTemplate.id == template_id
    ).first()
