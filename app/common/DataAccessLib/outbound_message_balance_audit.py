from DataAccessLib.common.utility import SingletonDecorator
from DataAccessLib.connection_network import ConnectionNetwork
from DataAccessLib.database.MySQL.outbound_message_audit_balance import (
    get_multiple_account_outbound_message_latest_audit)
from DataAccessLib.database.connect import SessionHandler
from DataAccessLib.handler import Getter


@SingletonDecorator
class ManageAccountOutboundMessageBalanceAudit:
    """
    This class is used to manage the account outbound message audit operations.
    """

    def __init__(self):
        self.config = ConnectionNetwork()

    def get_multiple_account_outbound_message_latest_audit(self, account_ids, today_date):
        """
        This method is used to fetch account latest outbound message audit.

        :param account_ids: LIST: Unique account ids
        :param today_date: DATE: Today date
        :return: Account latest outbound message audit
        """

        mysql_data = GetAccountOutboundMessageLatestAudit.get_data_from_sql(self.config.db_session,
                                                                            account_ids=account_ids,
                                                                            today_date=today_date)
        return GetAccountOutboundMessageLatestAudit.prepare_sync_payload(mysql_data, None)


class GetAccountOutboundMessageLatestAudit(Getter):

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
        with SessionHandler(db_session) as db_conn:
            outbound_message_audits = get_multiple_account_outbound_message_latest_audit(db_conn,
                                                                                         kwargs.get("account_ids"),
                                                                                         kwargs.get("today_date"))
            return dict(outbound_message_audits=outbound_message_audits)

    @staticmethod
    def prepare_sync_payload(data, es_result, **kwargs):
        """
        It will prepare payload.

        Required parameters:
            :param data: <<Class object>>: Data fetched from the SQL
            :param es_result: <<Object>>: Data fetched from the elasticsearch

        Optional parameters:
            :param kwargs: Any extra arguments

        :return: Object
        """
        account_audit_details = {}
        outbound_message_audits = data.get('outbound_message_audits')
        for outbound_message_audit in outbound_message_audits:
            account_id = str(outbound_message_audit.account_id)
            account_audit_details[account_id] = {
                "id": outbound_message_audit.id,
                "account_id": outbound_message_audit.account_id,
                "plan_id": outbound_message_audit.plan_id,
                "start_at": outbound_message_audit.start_at,
                "end_at": outbound_message_audit.end_at,
                "outbound_message_balance": outbound_message_audit.outbound_message_balance,
                "outbound_message_remaining_balance": outbound_message_audit.outbound_message_remaining_balance,
            }
        return account_audit_details
