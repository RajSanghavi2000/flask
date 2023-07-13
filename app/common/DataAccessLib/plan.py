from DataAccessLib.common.utility import add_log, SingletonDecorator
from DataAccessLib.connection_network import ConnectionNetwork
from DataAccessLib.database.MySQL.plan import get_plans_by_economical_priority
from DataAccessLib.database.connect import SessionHandler
from DataAccessLib.handler import Getter


@SingletonDecorator
class ManagePlansByEconomicalPriority:
    """
    This class is used to get the plans by economical priority from MysQL.

    """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_plans_with_economical_priority(self):
        """
        This method is used to get the plans by economical priority from MysQL.

        :return: plans by economical priority
        """

        mysql_data = GetPlansByEconomicalPriority.get_data_from_sql(self.config.db_session)
        return GetPlansByEconomicalPriority.prepare_sync_payload(mysql_data, None)


class GetPlansByEconomicalPriority(Getter):

    @staticmethod
    def get_data_from_sql(db_session, logger=None, **kwargs):
        """
        This method is used to fetch data from the SQL database.

        Required parameters:
            :param db_session: <<Class object>>

        Optional Parameters:
            :param logger: <<Class object>>
            :param kwargs: Extra arguments

        :return: Data if found else empty list []
        """
        with SessionHandler(db_session) as db_conn:
            plans = get_plans_by_economical_priority(conn=db_conn)
        if plans:
            return plans
        add_log(logger, "No data in SQL database")
        return []

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
        payload = {
            "plans": []
        }

        for plan in data:
            payload['plans'].append(plan.plan_id)

        return payload
