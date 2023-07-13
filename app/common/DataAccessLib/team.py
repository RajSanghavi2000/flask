from CachingLib import RedisOperationsTypeEnum

from DataAccessLib.common.enum import RedisKeyEnum
from DataAccessLib.common.utility import add_log, SingletonDecorator
from DataAccessLib.connection_network import ConnectionNetwork
from DataAccessLib.database.MySQL.team import get_team_members
from DataAccessLib.database.connect import SessionHandler
from DataAccessLib.handler import Getter, SyncDataHandler


@SingletonDecorator
class ManageTeamMember:
    """
    This class is used to manage the team member operations. It has different type of Get methods to fetch the team
    member related data.

     Get Team member methods will follow below process.
        1. Get data from Cache
        2. If data not found then Invoke ``sync_data`` method of class "SyncDataHandler" to fetch the data from SQL
        and set in Cache.
    """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_team_members(self, team_id):
        """
        This method is used to fetch team members.

        :param team_id: INTEGER: Unique team id
        :return: Team member data if data found in Cache or SQL database else empty response
        """

        key = RedisKeyEnum.TEAM_DATA.value.format(team_id=team_id)
        data = GetTeamMembers.get_data_from_cache(cache_conn=self.config.cache_conn, key=key)
        if not data:
            add_log(self.config.logger, "Data for key `{key}` not found in cache".format(key=key))
            add_log(self.config.logger,
                    "Fetching data from SQL database for team: {team_id}".format(team_id=team_id))

            data = SyncDataHandler.sync_data(self.config.db_session, self.config.cache_conn,
                                             GetTeamMembers, key, team_id=team_id, logger=self.config.logger)
        return data


class GetTeamMembers(Getter):
    @staticmethod
    def get_data_from_cache(cache_conn, key, **kwargs):
        """
        This method is used to fetch data from the Cache database.

        Required parameters:
            :param cache_conn: <<Class object>>
            :param key: STRING

        Optional parameters: It can be pass as a kwargs.

        :return Data if data found else None
        """

        return cache_conn.get(operation_type=RedisOperationsTypeEnum.GET_JSON.value,
                              payload={"key": key})

    @staticmethod
    def get_data_from_sql(db_session, logger=None, **kwargs):
        """
        This method is used to fetch data from the SQL database.

        Required parameters:
            :param db_session: <<Class object>>

        Optional Parameters:
            :param logger: <<Class object>>
            :param kwargs: Extra arguments

        :return: Data if found else empty object {}
        """
        team_members = []
        with SessionHandler(db_session) as db_conn:
            team_member_list = get_team_members(conn=db_conn, team_id=kwargs.get("team_id"))
        if team_member_list:
            for member in team_member_list:
                team_members.append("agent_{}".format(member.user_id))
            return dict(team_members=team_members)
        add_log(logger, "No data for team {team_id} in SQL database".format(team_id=kwargs.get("team_id")))

    @staticmethod
    def get_data_from_elasticsearch(logger=None, **kwargs):
        """
        Its overriding base class method ``get_data_from_elasticsearch``. Here we don't require to fetch anything from
        the elastic search so it will return empty object
        """
        return {}

    @staticmethod
    def prepare_sync_payload(data, es_result, **kwargs):
        """
        It will prepare payload to add data in Cache storage.

        Required parameters:
            :param data: <<Class object>>: Data fetched from the SQL
            :param es_result: <<Object>>: Data fetched from the elasticsearch

        Optional parameters:
            :param kwargs: Any extra arguments

        :return: Object
        """

        team_members = data.get("team_members")
        return dict(members=team_members)
