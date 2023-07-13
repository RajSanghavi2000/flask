from DataAccessLib.database.models import AdminConfiguration


def get_admin_configuration_details(conn):
    """
    SQLAlchemy query to fetch the Admin configuration data from SQL database.
    Required parameters:
       :param conn: <<Class object>>: SQL connection object
    :return: Theme configuration Data
   """
    return conn.query(AdminConfiguration).with_entities(
        AdminConfiguration.theme_configuration,
        AdminConfiguration.helpdesk_configuration,
        AdminConfiguration.sendgrid_branding_configuration,
        AdminConfiguration.custom_domain,
        AdminConfiguration.sendgrid_details,
        AdminConfiguration.general_branding
    ).order_by(AdminConfiguration.id.desc()).first()