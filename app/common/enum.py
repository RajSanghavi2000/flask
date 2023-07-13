from enum import Enum

__all__ = ['RedisKeyEnum', 'QueueEnum', 'StatusCodeEnum', 'SchemaKeysEnum']


class RedisKeyEnum(Enum):
    PERSON = "{person_id}_sample_person"


class QueueEnum(Enum):
    SAMPLE_PERSON = {'routing_key': 'sample_person', 'queue': 'sample_person_q',
                     'worker_count': 1, 'exchange_type': 'direct', 'exchange': 'wotnot.direct'}


class StatusCodeEnum(Enum):
    SUCCESS = 200
    CREATED_RESPONSE = 201


class SchemaKeysEnum(Enum):
    HEADER = 'header'
    ARGUMENTS = 'arguments'
    JSON = 'json'
    FORM = 'form'
    VIEW_ARGUMENTS = 'view_arguments'
    FILES = 'files'
