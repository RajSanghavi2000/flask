from DataAccessLib.database.models import (TeamMember)


def get_team_members(conn, team_id):
    """
    SQLAlchemy query to get team members of the team
    Required parameters:

       :param conn: <<Class object>>: SQL connection object
       :param team_id: INTEGER: Unique account id
    :return: Preview redis key
    """
    return conn.query(TeamMember).with_entities(
        TeamMember.user_id
    ).filter(
        TeamMember.team_id == team_id
    ).all()
