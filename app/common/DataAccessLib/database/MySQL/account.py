from UtilsLib import (UserTypeMasterEnum, FeaturesEnum, ChannelIdEnum)
from sqlalchemy import func, and_
from sqlalchemy.dialects.mysql import (CHAR, BINARY)
from sqlalchemy.sql.expression import cast

from DataAccessLib.common.constants import BOT_TYPES
from DataAccessLib.database.models import (Account,
                                           AccountSettings, PopupMessagePreferences, Bot,
                                           User, UserRole, Subscription, Plan,
                                           SubscriptionFeatureMapping, Feature,
                                           PopUpMessage, ConversationBalanceAudit, ChannelConfiguration, DeleteAccount,
                                           Visitor, ContactList)


def get_account_details(conn, account_ids):
    """
    SQLAlchemy query to fetch the Account data from SQL database.

    Required parameters:
       :param conn: <<Class object>>: SQL connection object
       :param account_ids: LIST<INTEGER>: Unique account ids

    :return: Account Data
   """
    return conn.query(Account).with_entities(
        Account.name.label("account_name"),
        Account.key.label("account_key"),
        Account.id.label("account_id"),
        Account.owner_id,
        Account.timezone,
        Account.payment_method,
        Account.image_name,
        Account.status.label("account_status"),
        AccountSettings.operating_hours,
        AccountSettings.enabled_human_handover,
        AccountSettings.maximum_chat_allocation_limit,
        AccountSettings.returning_user_cookie_duration,
        AccountSettings.feature_integration,
        AccountSettings.feature_configuration,
        AccountSettings.live_chat_configurations,
        AccountSettings.is_unassign_conversation_on_auto_assignment_failure_enabled,
        AccountSettings.outbound_configuration,
        func.json_extract(ChannelConfiguration.configuration, '$."is_domain_restricted"').label("is_domain_restricted"),
        func.json_extract(ChannelConfiguration.configuration, '$."registered_domains"').label("registered_domains"),
        func.json_extract(ChannelConfiguration.configuration, '$."site_url"').label("site_url"),
        PopupMessagePreferences.trigger_event,
        Subscription.id.label("subscription_id"),
        Subscription.plan_id,
        Plan.name.label("plan_name"),
        Plan.source.label("plan_source")
    ).join(
        Subscription, Account.id == Subscription.account_id
    ).join(
        Plan, Subscription.plan_id == Plan.id
    ).outerjoin(
        ChannelConfiguration, and_(Account.id == ChannelConfiguration.account_id,
                                   ChannelConfiguration.channel_id == ChannelIdEnum.WEB.value)
    ).outerjoin(
        AccountSettings, AccountSettings.account_id == Account.id
    ).outerjoin(
        PopupMessagePreferences, PopupMessagePreferences.account_id == Account.id
    ).filter(Account.id.in_(tuple(account_ids))).all()


def get_bot_list(conn, account_ids, include_deleted_bots=False):
    """
    SQLAlchemy query to get bot list of the account
    Required parameters:

       :param conn: <<Class object>>: SQL connection object
       :param account_ids: LIST<INTEGER>: Unique account id
       :param include_deleted_bots: Integer Include Deleted Bot as well
    :return: Preview redis key
    """
    if not include_deleted_bots:
        return conn.query(Bot).with_entities(
            Bot.id,
            Bot.is_deleted,
            Bot.account_id
        ).filter(Bot.account_id.in_(tuple(account_ids)), Bot.is_deleted == 0).order_by(Bot.created_at).all()

    return conn.query(Bot).with_entities(
        Bot.id,
        Bot.is_deleted,
        Bot.account_id
    ).filter(Bot.account_id.in_(tuple(account_ids))).order_by(Bot.created_at).all()


def get_account_users(conn, account_id):
    """
    SQLAlchemy query to get users of the account
    Required parameters:

       :param conn: <<Class object>>: SQL connection object
       :param account_id: INTEGER: Unique account id
    :return: list of account users
    """
    return conn.query(User).with_entities(
        User.id
    ).join(
        UserRole, UserRole.user_id == User.id
    ).filter(
        and_(
            UserRole.account_id == account_id,
            User.user_type_master_id == UserTypeMasterEnum.USER.value)
    ).order_by(
        cast(User.first_name, CHAR(charset='utf8')),
        cast(User.first_name, BINARY()).desc(),
        cast(User.last_name, CHAR(charset='utf8')),
        cast(User.last_name, BINARY()).desc(),
        cast(User.email, CHAR(charset='utf8')),
        cast(User.email, BINARY()).desc(),
    ).all()


def get_account_bots(conn, account_id, bot_type=BOT_TYPES):
    """
    SQLAlchemy query to get bot list of the account
    Required parameters:

       :param conn: <<Class object>>: SQL connection object
       :param account_id: INTEGER: Unique account id
       :param bot_type: TUPLE: bot type
    :return: Preview redis key
    """
    return conn.query(Bot).with_entities(
        Bot.id
    ).filter(and_(Bot.account_id == account_id, Bot.type.in_(tuple(bot_type)))).order_by(Bot.created_at).all()


def get_multiple_account_bots(conn, account_ids, bot_type=BOT_TYPES):
    """
    SQLAlchemy query to get bot list of the multiple accounts
    Required parameters:

       :param conn: <<Class object>>: SQL connection object
       :param account_ids: LIST: Unique account ids
       :param bot_type: TUPLE: bot type
    :return: Preview redis key
    """
    return conn.query(Bot).with_entities(
        Bot.id,
        Bot.account_id
    ).filter(and_(Bot.account_id.in_(tuple(account_ids)), Bot.type.in_(tuple(bot_type)))).order_by(Bot.created_at).all()


def get_account_features(conn, account_ids):
    """
    SQLAlchemy query to get features of the account
    Required parameters:

       :param conn: <<Class object>>: SQL connection object
       :param account_ids: INTEGER: Unique account ids
    :return: features
    """
    return conn.query(SubscriptionFeatureMapping).with_entities(
        SubscriptionFeatureMapping.config,
        SubscriptionFeatureMapping.feature_id,
        Feature.key,
        Subscription.account_id
    ).join(
        Subscription, Subscription.id == SubscriptionFeatureMapping.subscription_id
    ).join(
        Feature, Feature.id == SubscriptionFeatureMapping.feature_id
    ).filter(Subscription.account_id.in_(tuple(account_ids))).all()


def get_account_popup_messages(conn, account_ids):
    """
    SQLAlchemy query to get popup messages of the account
    Required parameters:

       :param conn: <<Class object>>: SQL connection object
       :param account_ids: LISt<INTEGER>: Unique account ids
    :return: popup_messages
    """
    return conn.query(PopUpMessage).with_entities(
        PopUpMessage.id,
        PopUpMessage.url_regex,
        PopUpMessage.message,
        PopUpMessage.account_id
    ).filter(PopUpMessage.account_id.in_(tuple(account_ids))).all()


def get_outbound_messages_total_balance(conn, account_id):
    """
    SQLAlchemy query to get outbound messages total balance:

       :param conn: <<Class object>>: SQL connection object
       :param account_id: INTEGER: Unique subscription id
    :return: outbound messages total balance
    """
    return conn.query(SubscriptionFeatureMapping).with_entities(
        SubscriptionFeatureMapping.config,
        ConversationBalanceAudit.start_at,
        ConversationBalanceAudit.end_at
    ).join(
        Subscription, Subscription.id == SubscriptionFeatureMapping.subscription_id
    ).join(
        Feature, Feature.id == SubscriptionFeatureMapping.feature_id
    ).join(
        ConversationBalanceAudit, ConversationBalanceAudit.account_id == Subscription.account_id
    ).filter(Subscription.account_id == account_id, Feature.key == FeaturesEnum.OUTBOUND.value
             ).order_by(ConversationBalanceAudit.id.desc()).limit(1).first()


def get_account_delete_resource(conn, account_id):
    """
      SQLAlchemy query to get outbound messages total balance:
      :param conn: <<Class object>>: SQL connection object
       :param account_id: INTEGER: Unique subscription id
    :return: outbound messages total balance
    """

    return conn.query(DeleteAccount).with_entities(
        DeleteAccount.resource_status.label('resources')
    ).filter(DeleteAccount.account_id == account_id).first()


def get_account_resource_stats(conn, account_id, resource):
    """
      SQLAlchemy query to get resource statistics :
      :param conn: <<Class object>>: SQL connection object
       :param account_id: INTEGER: Unique subscription id
       :param resource: Resource
    :return: get resource statistics
    """
    resource = '$."{}"'.format(resource)
    return conn.query(DeleteAccount).with_entities(
        func.json_extract(DeleteAccount.statistic, resource).label("resource")
    ).filter(DeleteAccount.account_id == account_id).first()


def get_account_total_visitor_count(conn, account_id):
    """
      SQLAlchemy query to get account total visitor count:
      :param conn: <<Class object>>: SQL connection object
       :param account_id: INTEGER: Unique account id
    :return: get visitor count
    """
    return conn.query(Visitor).with_entities(
        func.count(Visitor.id).label("count")
    ).filter(Visitor.account_id == account_id).first()

def get_contact_lists(conn, account_id):
    """
        SQLAlchemy query to get account contact lists:
        :param conn: <<Class object>>: SQL connection object
        :param account_id: INTEGER: Unique account id
        :return: get contact lists
    """
    return conn.query(ContactList).with_entities(
        ContactList.id, ContactList.name, ContactList.is_editable, ContactList.account_id, ContactList.is_deleted
    ).filter(and_(ContactList.account_id == account_id)).order_by(ContactList.created_at).all()


def fetch_account_id_by_account_key(conn, account_key):
    """
    SQLAlchemy query to fetch account_id
    Required parameters:
       :param conn: <<Class object>>: SQL connection object
       :param account_key: STRING
    :return: account_id
    """
    account_id = conn.query(Account).with_entities(Account.id).filter(Account.key == account_key).first()
    return account_id[0] if account_id else None
