from DataAccessLib.database.models import (GuideLinks)


def get_guide_links_data(conn):
    """
    SQLAlchemy query to fetch the guide links data from SQL database.

    Required parameters:
       :param conn: <<Class object>>: SQL connection object

    :return: guide links
   """
    records = conn.query(GuideLinks).with_entities(
        GuideLinks.key.label("key"),
        GuideLinks.name.label("name"),
        GuideLinks.url.label('url'),
        GuideLinks.id.label('id')
    ).all()

    return [record._asdict() for record in records]
