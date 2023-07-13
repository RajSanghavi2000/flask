from enum import Enum
from .constants import LANGUAGE, WEB_URL, DATE_RANGE
from .exceptions import (FieldRequiredException, StringInvalidException, AwareDateTimeInvalidException,
                         IPInterfaceInvalidException, IPv4InterfaceInvalidException, IPv6InterfaceInvalidException,
                         BooleanInvalidException, ChoiceInvalidException, IntegerInvalidException,
                         LengthInvalidException, PatternInvalidException, MappingInvalidException, UrlInvalidException,
                         NumberInvalidException, SchemaTypeInvalidException, PredicateInvalidException,
                         DateInvalidFormatException, TimeInvalidFormatException, DateTimeInvalidException,
                         ListInvalidException, NestedInvalidException, InputInvalidException, DateInvalidException,
                         IPInvalidException, UUIDInvalidException, TimeInvalidException, FieldNullException,
                         FieldUnknownException, IPv4InvalidException, TupleInvalidException, FloatSpecialException,
                         IPv6InvalidException, ChoicesInvalidException, RangeInvalidLowerInclusiveHigherException,
                         LengthInvalidBetweenException, RangeInvalidHigherException, RangeInvalidLowerHigherException,
                         RangeInvalidLowerException, LengthInvalidHigherException, LengthInvalidLowerException,
                         NumberTooLargeException, TimeDeltaInvalidException, RangeInvalidLowerHigherInclusiveException,
                         StringInvalidUtf8Exception, DateTimeInvalidFormatException, NaiveDateTimeInvalidException,
                         TimeDeltaInvalidFormatException, RangeInvalidHigherInclusiveException, EmailInvalidException,
                         RangeInvalidLowerInclusiveException, RangeInvalidLowerInclusiveHigherInclusiveException)

__all__ = ['ChannelIdEnum', 'ChannelNameEnum', 'SchemaKeysEnum', 'WhatsappChannelProviderNameEnum',
           'WhatsappChannelProviderIdEnum', 'StorageProvider', 'HttpMethodEnum', 'RequestBodyType', 'UserTypeMasterEnum',
           'ConversationStatusEnum', "ConversationBalanceDeductionProcessStatusEnum",
           "ConversationBalanceAuditTypeEnum", "FeaturesEnum", "SortingOrderEnum", "ContactDataViewEnum",
           "DayNumericValueEnum", 'FileTypesGroupEnum', 'UserTypeEnum', 'NotificationEventsEnum', 'ChannelTriggerRulesEnum',
           'TriggerRulesOperatorEnum', 'MessagesStatusFieldEnum', 'BotTypeEnum', 'StatusCodeEnum',
           'TemplateStatus', 'SMSChannelProviderIdEnum', 'SMSChannelProviderNameEnum', 'FileTypesEnum',
           'SendMessageDialogTypeEnum', 'VersionEnum', 'SendMessageTypeEnum', 'ChannelMappingEnum',
           'GlobalChannelNameEnum',
           'OutboundBotStatusEnum', 'PaymentMethodEnum', 'TriggerFieldsEnum', 'TriggerRuleFiltersEnum',
           'DynamicListEnum', 'TriggerRuleOperatorsCountEnum', 'ChannelTriggerRulesEnumV2', 'VariableFormatEnum',
           'VariableTypeEnum', 'EsLatestConFieldsPrefix', 'EventType', 'VariableStatusEnum',
           'VariableTypeBranchOperatorEnum', 'AppVersionEnum', "ErrorRegexAndResponseEnum",
           'TriggerRulesWebUrlOperatorEnum', 'CloudUploadMediaURLEnum', 'DialogEventType', 'DialogTypeEnum',
           'Dialog360Environments']


class ChannelIdEnum(Enum):
    WEB = 1
    WEB_PREVIEW = 2
    FACEBOOK_MESSENGER = 3
    SMS = 4
    WHATSAPP = 5
    VOICEWEB = 7


class ChannelNameEnum(Enum):
    WEB = "WEB"
    WEB_PREVIEW = "WEB_PREVIEW"
    FACEBOOK_MESSENGER = "FACEBOOK_MESSENGER"
    SMS = "SMS"
    WHATSAPP = "WHATSAPP"
    VOICEWEB = "VOICEWEB"


class SchemaKeysEnum(Enum):
    HEADER = 'header'
    ARGUMENTS = 'arguments'
    JSON = 'json'
    FORM = 'form'
    VIEW_ARGUMENTS = 'view_arguments'
    FILES = 'files'


class WhatsappChannelProviderNameEnum(Enum):
    TWILIO = "Twilio"
    GUPSHUP = "Gupshup"
    DIALOG_360 = '360Dialog'
    UNIFONIC = 'Unifonic'
    META = 'Meta'
    DIALOG_360_CLOUD = '360Dialog Cloud'


class SMSChannelProviderNameEnum(Enum):
    TWILIO = "Twilio"
    TWILIO_MANAGED = "Twilio Managed"
    TECH_ALPHA = "TechAlpha"


class WhatsappChannelProviderIdEnum(Enum):
    UNIFONIC = 2
    TWILIO = 3
    GUPSHUP = 4
    DIALOG360 = 5
    META = 8
    DIALOG360CLOUD = 10


class SMSChannelProviderIdEnum(Enum):
    TWILIO = 6
    TWILIO_MANAGED = 7
    TECH_ALPHA = 9


class StorageProvider(Enum):
    GCP = 'gcp'
    S3 = 's3'
    REGION = 'auto'
    GCP_ENDPOINT_URL = "https://storage.googleapis.com"
    LOCAL_STORAGE = 'local_storage'
    AZURE = 'azure'


class HttpMethodEnum(Enum):
    POST = 'POST'
    PUT = 'PUT'
    GET = 'GET'
    DELETE = 'DELETE'
    PATCH = 'PATCH'


class RequestBodyType(Enum):
    RAW = 'raw'
    FORM = 'form'


class UserTypeMasterEnum(Enum):
    USER = 1
    BOT = 2


class UserTypeEnum(Enum):
    USER = "user"
    BOT = "bot"


class NotificationEventsEnum(Enum):
    HUMAN_HANDOVER = 'human_handover'
    NEW_OPEN_MESSAGE = 'new_open_message'


class ConversationStatusEnum(Enum):
    OPEN = 1
    CLOSE = 2


class ConversationBalanceDeductionProcessStatusEnum(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class ConversationBalanceAuditTypeEnum(Enum):
    MONTHLY = "Monthly"
    ADDITIONAL = "Additional"


class FeaturesEnum(Enum):
    ADD_USERS = "add_users"
    TEAM_MANAGEMENT = "team_management"
    TEAMMATE_MANAGEMENT = "teammate_management"
    SINGLE_SIGN_ON = "single_sign_on"
    PREMIUM_THEMES = "premium_themes"
    THEMEING_CHAT_WIDGET = "themeing_chat_widget"
    CUSTOMIZE_WIDGET_ICON = "customize_widget_icon"
    REMOVE_BRANDING = "remove_branding"
    RICH_MEDIA_SUPPORT = "rich_media_support"
    MULTI_LINGUAL = "multi_lingual"
    LOGICAL_FLOW = "logical_flow"
    TEMPLATES_REPOSITORY = "templates_repository"
    TRIGGER_CONDITIONS = "trigger_conditions"
    HISTORY_RETENTION = "history_retention"
    CHAT_INTERFACE_CUSTOM_VISIBILITY = "chat_interface_custom_visibility"
    FIRE_JAVASCRIPTS = "fire_javascripts"
    HUMAN_HANDOVER = "human_handover"
    DATA_INJECTION = "data_injection"
    FAQ_BUILDER = "faq_builder"
    AGENT_SEATS = "agent_seats"
    SAVED_REPLIES = "saved_replies"
    CONVERSATION_LABLES = "conversation_lables"
    RELATED_CONVERSATIONS = "related_conversations"
    TEAMMATE_AVAILABILITY = "teammate_availability"
    MANUAL_REASSIGNMENT = "manual_reassignment"
    AGENT_NOTES = "agent_notes"
    ONE_CLICK_CHAT_TRANSCRIPTS = "one_click_chat_transcripts"
    MOBILE_APP = "mobile_app"
    VISITOR_DETAILS = "visitor_details"
    CONVERSATION_ROUND_ROBIN_ASSIGNMENTS = "conversation_round_robin_assignments"
    CONVERSATION_TEAM_ASSIGNMENTS = "conversation_team_assignments"
    AGENT_MAX_CHAT_LIMITS = "agent_max_chat_limits"
    HELP_DOCS = "help_docs"
    VIDEO_TUTORIALS = "video_tutorials"
    CUSTOMER_EMAIL_SUPPORT = "customer_email_support"
    CUSTOMER_CALL_SUPPORT = "customer_call_support"
    PERSONALIZED_ONBOARDING = "personalized_onboarding"
    IMPLEMENTATION_ASSISTANCE_AND_TRAINING = "implementation_assistance_and_training"
    DEDICATED_CUSTOMER_SUCCESS_MANAGER = "dedicated_customer_success_manager"
    PRIORITIZED_SUPPORT = "24_7_prioritized_support"
    OPTIMIZATION_SERVICES = "optimization_services"
    TECHNICAL_INTEGRATION_SETUP = "technical_integration_setup"
    DEDICATED_SUPPORT_ASSISTANCE = "dedicated_support_assistance"
    SLACK_INTEGRATION = "slack_integration"
    WORDPRESS_INTEGRATION = "wordpress_integration"
    DIALOGFLOW_INTEGRATION = "dialogflow_integration"
    IBM_WATSON_INTEGRATION = "ibm_watson_integration"
    FOLLOW_UP_BOSS_INTEGRATION = "follow_up_boss_integration"
    SALESFORCE_INTEGRATION = "salesforce_integration"
    HUBSPOT_INTEGRATION = "hubspot_integration"
    ZOHO_INTEGRATION = "zoho_integration"
    GOOGLE_CALENDAR_INTEGRATION = "google_calendar_integration"
    AIRTABLE_INTEGRATION = "airtable_integration"
    QUICKBOOKS_INTEGRATION = "quickbooks_integration"
    DATA_STUDIO_INTEGRATION = "data_studio_integration"
    ANALYTICS_DASHBOARD_ACCESS = "analytics_dashboard_access"
    DISPLAY_LEAD_DATA = "display_lead_data"
    CONVERSATION_EXPORT = "conversation_export"
    ANNUAL_PERFORMANCE_REPORT = "annual_performance_report"
    ANALYSIS_ASSISTANCE = "analysis_assistance"
    CUSTOM_KPI_CARDS = "custom_kpi_cards"
    CONVERSATIONS = "conversations"
    CREATE_BOTS = "create_bots"
    CALENDLY_INTEGRATION = "calendly_integration"
    GOOGLE_SHEET_INTEGRATION = "google_sheets_integration"
    CUSTOM_CSS = "custom_css"
    OUTBOUND = "outbound"
    ANONYMIZE_FACEBOOK_VISITOR = "anonymize_facebook_visitor"
    ZAPIER_INTEGRATION = "zapier_integration"
    FRESHDESK_INTEGRATION = "freshdesk_integration"
    CODEBLOCK = "codeblock"
    ACTIVECAMPAIGN_INTEGRATION = "activecampaign_integration"
    OPEN_AI = "open_ai_integration"


class SortingOrderEnum(Enum):
    ASC = "asc"
    DESC = "desc"


class ContactDataViewEnum(Enum):
    CONVERSATION = "conversation"
    VISITOR = "visitor"


class DayNumericValueEnum(Enum):
    NULL = None
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class FileTypesGroupEnum(Enum):
    VIDEO = 'video'
    IMAGE = 'image'
    DOCUMENT = 'document'


class FileTypesEnum(Enum):
    VIDEO = 'video'
    IMAGE = 'image'
    DOCUMENT = 'document'
    AUDIO = 'audio'


class BotTypeEnum(Enum):
    INBOUND = 'inbound'
    OUTBOUND = 'outbound'


class PaymentMethodEnum(Enum):
    MANUAL = "manual"
    AUTOMATIC = "automatic"


class ChannelTriggerRulesEnum(Enum):
    WEB = [LANGUAGE, WEB_URL, DATE_RANGE]
    WEB_PREVIEW = [LANGUAGE, WEB_URL, DATE_RANGE]
    TWILIO = [DATE_RANGE]
    MESSENGER = [DATE_RANGE]
    WHATSAPP = [DATE_RANGE]
    SMS = [DATE_RANGE]

    ID_TO_NAME_LINK = {
        ChannelIdEnum.FACEBOOK_MESSENGER.value: 'MESSENGER',
        ChannelIdEnum.WEB.value: 'WEB',
        ChannelIdEnum.WEB_PREVIEW.value: 'WEB_PREVIEW',
        ChannelIdEnum.WHATSAPP.value: 'WHATSAPP',
        ChannelIdEnum.VOICEWEB.value: 'VOICEWEB',
        ChannelIdEnum.SMS.value: 'SMS'
    }
    NAME_TO_ID_LINK = {
        'MESSENGER': ChannelIdEnum.FACEBOOK_MESSENGER.value,
        'WEB': ChannelIdEnum.WEB.value,
        'WEB_PREVIEW': ChannelIdEnum.WEB_PREVIEW.value,
        'WHATSAPP': ChannelIdEnum.WHATSAPP.value,
        'VOICEWEB': ChannelIdEnum.VOICEWEB.value,
    }


class ChannelTriggerRulesEnumV2(Enum):
    WEB = [DATE_RANGE, LANGUAGE, WEB_URL]
    WEB_PREVIEW = [DATE_RANGE, LANGUAGE, WEB_URL]
    TWILIO = [DATE_RANGE]
    MESSENGER = [DATE_RANGE]
    WHATSAPP = [DATE_RANGE]
    SMS = [DATE_RANGE]

    ID_TO_NAME_LINK = {
        ChannelIdEnum.FACEBOOK_MESSENGER.value: 'MESSENGER',
        ChannelIdEnum.WEB.value: 'WEB',
        ChannelIdEnum.WEB_PREVIEW.value: 'WEB_PREVIEW',
        ChannelIdEnum.WHATSAPP.value: 'WHATSAPP',
        ChannelIdEnum.VOICEWEB.value: 'VOICEWEB',
        ChannelIdEnum.SMS.value: 'SMS'
    }
    NAME_TO_ID_LINK = {
        'MESSENGER': ChannelIdEnum.FACEBOOK_MESSENGER.value,
        'WEB': ChannelIdEnum.WEB.value,
        'WEB_PREVIEW': ChannelIdEnum.WEB_PREVIEW.value,
        'WHATSAPP': ChannelIdEnum.WHATSAPP.value,
        'VOICEWEB': ChannelIdEnum.VOICEWEB.value,
    }


class TriggerRulesOperatorEnum(Enum):
    AND = "AND"
    OR = "OR"


class MessagesStatusFieldEnum(Enum):
    SENT_AT = 'sent_at'
    DELIVERED_AT = 'delivered_at'
    SEEN_AT = 'seen_at'
    REPLIED_AT = 'replied_at'
    FAILED_AT = 'failed_at'


class StatusCodeEnum(Enum):
    SUCCESS = 200
    CREATED_RESPONSE = 201
    BAD_REQUEST = 400
    SERVICE_UNAVAILABLE = 503
    RETRY = 429
    UNAUTHORIZED = 401


class TemplateStatus(Enum):
    INACTIVATED = 'inactivated'


class SendMessageDialogTypeEnum(Enum):
    TEXT = "text"
    VIDEO = 'video'
    IMAGE = 'image'
    DOCUMENT = 'document'
    AUDIO = 'audio'


class SendMessageTypeEnum(Enum):
    TEXT = "text"
    FILE = 'file'


class VersionEnum(Enum):
    VERSION_V1 = 1
    VERSION_V2 = 2


class GlobalChannelNameEnum(Enum):
    WEB = "Web"
    WEB_PREVIEW = "WEB_PREVIEW"
    FACEBOOK_MESSENGER = "Facebook"
    SMS = "SMS"
    WHATSAPP = "WhatsApp"
    VOICEWEB = "VoiceWeb"


class ChannelMappingEnum(Enum):
    ID_TO_NAME = {
        ChannelIdEnum.FACEBOOK_MESSENGER.value: 'MESSENGER',
        ChannelIdEnum.WEB.value: 'WEB',
        ChannelIdEnum.WEB_PREVIEW.value: 'WEB_PREVIEW',
        ChannelIdEnum.WHATSAPP.value: 'WHATSAPP',
        ChannelIdEnum.VOICEWEB.value: 'VOICEWEB',
        ChannelIdEnum.SMS.value: 'SMS'
    }

    ID_TO_GLOBAL_NAME = {
        ChannelIdEnum.FACEBOOK_MESSENGER.value: GlobalChannelNameEnum.FACEBOOK_MESSENGER.value,
        ChannelIdEnum.WEB.value: GlobalChannelNameEnum.WEB.value,
        ChannelIdEnum.WEB_PREVIEW.value: GlobalChannelNameEnum.WEB.value,
        ChannelIdEnum.WHATSAPP.value: GlobalChannelNameEnum.WHATSAPP.value,
        ChannelIdEnum.SMS.value: GlobalChannelNameEnum.SMS.value,
        ChannelIdEnum.VOICEWEB.value: GlobalChannelNameEnum.VOICEWEB.value
    }


class OutboundBotStatusEnum(Enum):
    DRAFT = "Draft"
    RUNNING = "Running"
    SENT = "Sent"


class TriggerFieldsEnum(Enum):
    DATE = "date"
    LANGUAGE = "language"
    EXCLUDE_PATH = "exclude_path"
    INCLUDE_PATH = "include_path"
    DEFAULT = "default"


class TriggerRuleFiltersEnum(Enum):
    DATE_RANGE = "date_range"
    LANGUAGE = "language"
    WEB_URL = "web_url"


class TriggerRuleOperatorsCountEnum(Enum):
    AND = 1
    OR = 3


class DynamicListEnum(Enum):
    DEFAULT = "self"
    FIRST_NAME_PATTERN = ".{}"
    OTHER_NAME_PATTERN = "_{}"


class VariableFormatEnum(Enum):
    NAME = "name"
    EMAIL = "email"
    PHONE = "phone"
    NUMBER = "number"
    TEXT = "text"
    DATE = "date"
    REGEX = "regex"
    BOOLEAN = "boolean"


class EsLatestConFieldsPrefix(Enum):
    PARAM = "param__"
    VISITOR = "visitor_"


class VariableTypeEnum(Enum):
    CONTACT = "contact"
    SYSTEM = "system"
    CONVERSATION = "conversation"


class EventType(Enum):
    MESSAGE = 1
    NOTE = 2
    ASSIGNEE = 3
    STATUS = 4
    ACTION = 5
    ANALYTICS = 6
    VISITOR_QUALIFICATION = 7
    PARAMETER = 8
    MESSAGE_READ = 9
    BULK_PARAMETER = 10
    BULK_STATUS_CLOSE = 11
    SYNC_FIELDS = 12
    LAST_TRACK_GOAL = 13
    SLACK_LIVE_CHAT = 14


class VariableStatusEnum(Enum):
    ACTIVE = 'active'
    ARCHIVE = 'archive'


class VariableTypeBranchOperatorEnum(Enum):
    TEXT = {'equals_to', 'not_equals_to', 'contains', 'does_not_contain', 'is_empty', 'is_not_empty', 'in', 'not_in',
            'equal_to', 'not_equal_to'}
    NAME = {'equals_to', 'not_equals_to', 'contains', 'does_not_contain', 'is_empty', 'is_not_empty', 'in', 'not_in',
            'equal_to', 'not_equal_to'}
    EMAIL = {'equals_to', 'not_equals_to', 'contains', 'does_not_contain', 'is_empty', 'is_not_empty', 'in', 'not_in',
             'equal_to', 'not_equal_to'}
    PHONE = {'equals_to', 'not_equals_to', 'contains', 'does_not_contain', 'is_empty', 'is_not_empty', 'in', 'not_in',
             'equal_to', 'not_equal_to'}
    NUMBER = {'equals_to', 'not_equals_to', 'greater_than', 'less_than', 'greater_than_or_equal_to',
               'less_than_or_equal_to', 'in', 'not_in', 'equal_to', 'not_equal_to'}
    DATE = {'equals_to', 'not_equals_to', 'greater_than', 'less_than', 'greater_than_or_equal_to',
            'less_than_or_equal_to', 'in', 'not_in', 'equal_to', 'not_equal_to'}
    BOOLEAN = {'equals_to', 'not_equals_to', 'in', 'not_in', 'equal_to', 'not_equal_to'}
    REGEX = {'equals_to', 'not_equals_to', 'contains', 'does_not_contain', 'is_empty', 'is_not_empty',
             'greater_than', 'less_than', 'greater_than_or_equal_to', 'less_than_or_equal_to', 'matches_pattern',
             'does_not_match_pattern', 'in', 'not_in', 'equal_to', 'not_equal_to'}


class AppVersionEnum(Enum):
    PWA = 'PWA'
    REACT_NATIVE = 'react-native'


class CloudUploadMediaURLEnum(Enum):
    META = 'https://graph.facebook.com/v16.0/{}/media?messaging_product=whatsapp'
    DIALOG360 = 'https://waba.360dialog.io/v1/media'
    DIALOG360CLOUD = 'https://waba-v2.360dialog.io/media'
    

class ErrorRegexAndResponseEnum(Enum):
    FIELD_REQUIRED = {
        "regex": "Missing data for required field.",
        "message": "{var1} missing data for required field.",
        "exception": FieldRequiredException
    }
    STRING_INVALID = {
        "regex": "Not a valid string.",
        "message": "{var1} not a valid string.",
        "exception": StringInvalidException
    }
    INTEGER_INVALID = {
        "regex": "Not a valid integer.",
        "message": "{var1} not a valid integer.",
        "exception": IntegerInvalidException
    }
    STRING_INVALID_UTF8 = {
        "regex": "Not a valid utf-8 string.",
        "message": "{var1} not a valid utf-8 string.",
        "exception": StringInvalidUtf8Exception
    }
    RANGE_INVALID_LOWER_INCLUSIVE_HIGHER_INCLUSIVE = {
        "regex": "Must be greater than or equal to (\d+) and less than or equal to (\d+).",
        "message": "{var1} must be greater than or equal to {var2} and less than or equal to {var3}.",
        "exception": RangeInvalidLowerInclusiveHigherInclusiveException
    }
    RANGE_INVALID_LOWER_HIGHER_INCLUSIVE = {
        "regex": "Must be greater than (\d+) and less than or equal to (\d+).",
        "message": "{var1} must be greater than {var2} and less than or equal to {var3}.",
        "exception": RangeInvalidLowerHigherInclusiveException
    }
    RANGE_INVALID_LOWER_INCLUSIVE_HIGHER = {
        "regex": "Must be greater than or equal to (\d+) and less than (\d+).",
        "message": "{var1} must be greater than or equal to {var2} and less than {var3}.",
        "exception": RangeInvalidLowerInclusiveHigherException
    }
    RANGE_INVALID_LOWER_HIGHER = {
        "regex": "Must be greater than (\d+) and less than (\d+).",
        "message": "{var1} must be greater than {var2} and less than {var3}.",
        "exception": RangeInvalidLowerHigherException
    }
    RANGE_INVALID_LOWER_INCLUSIVE = {
        "regex": "Must be greater than or equal to (\d+).",
        "message": "{var1} must be greater than or equal to {var2}.",
        "exception": RangeInvalidLowerInclusiveException
    }
    RANGE_INVALID_LOWER = {
        "regex": "Must be greater than (\d+).",
        "message": "{var1} must be greater than {var2}.",
        "exception": RangeInvalidLowerException
    }
    RANGE_INVALID_HIGHER_INCLUSIVE = {
        "regex": "Must be less than or equal to (\d+).",
        "message": "{var1} must be less than or equal to {var2}.",
        "exception": RangeInvalidHigherInclusiveException
    }
    RANGE_INVALID_HIGHER = {
        "regex": "Must be less than (\d+).",
        "message": "{var1} must be less than {var2}.",
        "exception": RangeInvalidHigherException
    }
    FIELD_NULL = {
        "regex": "Field may not be null.",
        "message": "{var1} field may not be null.",
        "exception": FieldNullException
    }
    EMAIL_INVALID = {
        "regex": "Not a valid email address.",
        "message": "{var1} not a valid email address.",
        "exception": EmailInvalidException
    }

    LENGTH_INVALID_BETWEEN = {
        "regex": "Length must be between (\d+) and (\d+).",
        "message": "{var1} length must be between {var2} and {var3}.",
        "exception": LengthInvalidBetweenException
    }
    LENGTH_INVALID_LOWER = {
        "regex": "Shorter than minimum length (\d+).",
        "message": "{var1} shorter than minimum length {var2}.",
        "exception": LengthInvalidLowerException
    }
    LENGTH_INVALID_HIGHER = {
        "regex": "Longer than maximum length (\d+).",
        "message": "{var1} longer than maximum length {var2}.",
        "exception": LengthInvalidHigherException
    }
    LENGTH_INVALID = {
        "regex": "Length must be (\d+).",
        "message": "{var1} length must be {var2}.",
        "exception": LengthInvalidException
    }
    INPUT_INVALID = {
        "regex": "Must be equal to (\w+).",
        "message": "{var1} must be equal to {var2}.",
        "exception": InputInvalidException
    }
    PATTERN_INVALID = {
        "regex": "String does not match expected pattern.",
        "message": "{var1} string does not match expected pattern.",
        "exception": PatternInvalidException
    }
    IP_INVALID = {
        "regex": "Not a valid IP address.",
        "message": "{var1} not a valid IP address.",
        "exception": IPInvalidException
    }
    IPV4_INVALID = {
        "regex": "Not a valid IPv4 address.",
        "message": "{var1} not a valid IPv4 address.",
        "exception": IPv4InvalidException
    }
    IPV6_INVALID = {
        "regex": "Not a valid IPv6 address.",
        "message": "{var1} not a valid IPv6 address.",
        "exception": IPv6InvalidException
    }
    SCHEMA_TYPE_INVALID = {
        "regex": "Invalid input type.",
        "message": "{var1} invalid input type.",
        "exception": SchemaTypeInvalidException
    }
    PREDICATE_INVALID = {
        "regex": "Invalid input.",
        "message": "{var1} invalid input.",
        "exception": PredicateInvalidException
    }
    CHOICE_INVALID = {
        "regex": "Must be one of: ([\w+,.\s]+).",
        "message": "{var1} must be one of: {var2}.",
        "exception": ChoiceInvalidException
    }
    CHOICES_INVALID = {
        "regex": "One or more of the choices you made was not in: ([\w+,\s]+).",
        "message": "{var1} one or more of the choices you made was not in: {var2}.",
        "exception": ChoicesInvalidException
    }
    URL_INVALID = {
        "regex": "Not a valid URL.",
        "message": "{var1} not a valid URL.",
        "exception": UrlInvalidException
    }
    NESTED_INVALID = {
        "regex": "Invalid type.",
        "message": "{var1} invalid type.",
        "exception": NestedInvalidException
    }
    DATETIME_INVALID = {
        "regex": "Not a valid datetime.",
        "message": "{var1} not a valid datetime.",
        "exception": DateTimeInvalidException
    }
    NAIVE_DATETIME_INVALID = {
        "regex": "Not a valid naive datetime.",
        "message": "{var1} not a valid naive datetime.",
        "exception": NaiveDateTimeInvalidException
    }
    AWARE_DATETIME_INVALID = {
        "regex": "Not a valid aware datetime.",
        "message": "{var1} not a valid aware datetime.",
        "exception": AwareDateTimeInvalidException
    }
    TIME_INVALID = {
        "regex": "Not a valid time.",
        "message": "{var1} not a valid time.",
        "exception": TimeInvalidException
    }
    DATE_INVALID = {
        "regex": "Not a valid date.",
        "message": "{var1} not a valid date.",
        "exception": DateInvalidException
    }
    DATE_INVALID_FORMAT = {
        "regex": "\"[\w+]\" cannot be formatted as a date.",
        "message": "{var1} {var2} cannot be formatted as a date.",
        "exception": DateInvalidFormatException
    }
    DATETIME_INVALID_FORMAT = {
        "regex": "\"[\w+]\" cannot be formatted as a datetime.",
        "message": "{var1} {var2} cannot be formatted as a datetime.",
        "exception": DateTimeInvalidFormatException
    }
    TIME_INVALID_FORMAT = {
        "regex": "\"[\w+]\" cannot be formatted as a time.",
        "message": "{var1} {var2} cannot be formatted as a time.",
        "exception": TimeInvalidFormatException
    }
    LIST_INVALID = {
        "regex": "Not a valid list.",
        "message": "{var1} not a valid list.",
        "exception": ListInvalidException
    }
    TUPLE_INVALID = {
        "regex": "Not a valid tuple.",
        "message": "{var1} not a valid tuple.",
        "exception": TupleInvalidException
    }
    UUID_INVALID = {
        "regex": "Not a valid UUID.",
        "message": "{var1} not a valid UUID.",
        "exception": UUIDInvalidException
    }
    NUMBER_INVALID = {
        "regex": "Not a valid number.",
        "message": "{var1} not a valid number.",
        "exception": NumberInvalidException
    }
    NUMBER_TOO_LARGE = {
        "regex": "Number too large.",
        "message": "{var1} number too large.",
        "exception": NumberTooLargeException
    }
    FLOAT_SPECIAL = {
        "regex": "Special numeric values \(nan or infinity\) are not permitted.",
        "message": "{var1} special numeric values (nan or infinity) are not permitted.",
        "exception": FloatSpecialException
    }
    BOOLEAN_INVALID = {
        "regex": "Not a valid boolean.",
        "message": "{var1} not a valid boolean.",
        "exception": BooleanInvalidException
    }
    TIMEDELTA_INVALID = {
        "regex": "Not a valid period of time.",
        "message": "{var1} not a valid period of time.",
        "exception": TimeDeltaInvalidException
    }
    TIMEDELTA_INVALID_FORMAT = {
        "regex": "\"[\w+]\" cannot be formatted as a timedelta.",
        "message": "{var1} {var2} cannot be formatted as a timedelta.",
        "exception": TimeDeltaInvalidFormatException
    }
    MAPPING_INVALID = {
        "regex": "Not a valid mapping type.",
        "message": "{var1} not a valid mapping type.",
        "exception": MappingInvalidException
    }
    FIELD_UNKNOWN = {
        "regex": "Unknown field.",
        "message": "{var1} unknown field.",
        "exception": FieldUnknownException
    }
    IP_INTERFACE_INVALID = {
        "regex": "Not a valid IP interface.",
        "message": "{var1} not a valid IP interface.",
        "exception": IPInterfaceInvalidException
    }
    IPV4_INTERFACE_INVALID = {
        "regex": "Not a valid IPv4 interface.",
        "message": "{var1} not a valid IPv4 interface.",
        "exception": IPv4InterfaceInvalidException
    }
    IPV6_INTERFACE_INVALID = {
        "regex": "Not a valid IPv6 interface.",
        "message": "{var1} not a valid IPv6 interface.",
        "exception": IPv6InterfaceInvalidException
    }


class TriggerRulesWebUrlOperatorEnum(Enum):
    EQUALS_TO = "equals_to"
    NOT_EQUALS_TO = "not_equals_to"
    CONTAINS = "contains"
    DOES_NOT_CONTAIN = "does_not_contain"


class DialogEventType(Enum):
    MESSAGE = "message"
    TYPING = "typing"
    status = "status"
    assignee = "assignee"
    FAQ_FEEDBACK = "faq_feedback"


class DialogTypeEnum(Enum):
    SEND_MESSAGE = 'send_message'
    EMAIL = 'email'
    PHONE = 'phone'
    NAME = 'name'
    TEXT = 'text'
    BUTTON = 'button'
    CAROUSEL = 'carousel'
    IMAGE_CAROUSEL = 'image_carousel'
    FILE_UPLOAD = 'file_upload'
    CALENDAR = 'calendar'
    SLIDER = 'slider'
    FORM = 'form'
    DELAY = 'delay'
    JAVASCRIPT = "javascript"
    APPOINTMENT_BOOKING = "appointment_booking"
    LIST = "list"
    SEND_SMS = 'send_sms'


class Dialog360Environments(Enum):
    PRODUCTION = "PRODUCTION"
    SANDBOX = "SANDBOX"
