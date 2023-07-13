class InvalidRequestSchemaException(Exception):
    def __init__(self, message, code, payload):
        self.message = message
        self.code = code
        self.payload = payload


class BadRequestException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class FieldRequiredException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class StringInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class IntegerInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class StringInvalidUtf8Exception(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class RangeInvalidLowerInclusiveHigherInclusiveException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class RangeInvalidLowerHigherInclusiveException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class RangeInvalidLowerHigherException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class RangeInvalidLowerInclusiveHigherException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class RangeInvalidLowerInclusiveException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class RangeInvalidLowerException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class RangeInvalidHigherInclusiveException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class RangeInvalidHigherException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class FieldNullException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class EmailInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class LengthInvalidBetweenException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class LengthInvalidLowerException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class LengthInvalidHigherException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class LengthInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class InputInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class PatternInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class IPInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class IPv4InvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class IPv6InvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class SchemaTypeInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class PredicateInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class ChoiceInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class ChoicesInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class UrlInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class NestedInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class DateTimeInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class NaiveDateTimeInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class AwareDateTimeInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class TimeInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class DateInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class DateInvalidFormatException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class DateTimeInvalidFormatException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class TimeInvalidFormatException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class ListInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class TupleInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class UUIDInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class NumberInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class NumberTooLargeException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class FloatSpecialException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class BooleanInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class TimeDeltaInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class TimeDeltaInvalidFormatException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class MappingInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class FieldUnknownException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class IPInterfaceInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class IPv4InterfaceInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)


class IPv6InterfaceInvalidException(InvalidRequestSchemaException):
    def __init__(self, message, code, payload):
        super().__init__(message, code, payload)
