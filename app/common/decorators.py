from functools import wraps
from flask import Response
from marshmallow.exceptions import ValidationError
from .error import errors
from .utils import get_request_payload
from .schema import ErrorSchema
from dataclasses import dataclass, is_dataclass

__all__ = ['api_route', 'validate_api_schema', 'nested_dataclass']


def nested_dataclass(*args, **kwargs):
    """This decorator is used to create nested dataclass object"""

    def wrapper(cls):
        cls = dataclass(cls, **kwargs)
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            for name, value in kwargs.items():
                field_type = cls.__annotations__.get(name, None)
                if is_dataclass(field_type) and isinstance(value, dict):
                    new_obj = field_type(**value)
                    kwargs[name] = new_obj
            original_init(self, *args, **kwargs)

        cls.__init__ = __init__
        return cls

    return wrapper(args[0]) if args else wrapper


def api_route(self, *args, **kwargs):
    """Add endpoint class to the api resource"""

    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls

    return wrapper


def validate_api_schema(schema_key, schema_class, logger=None):
    """
    This method is used to validate api request headers, arguments and body of type json. It's using marshmallow to
    validate the schema. If request schema is invalid then it returns bad request error.

    :param schema_key: Request schema to validate. i.e headers, arguments, body
    :param schema_class: Marshmallow schema class
    :param logger: app logger object. Default None.
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            schema = schema_class()
            payload = get_request_payload(schema_key)
            try:
                payload = schema.dump(schema.load(payload))
                kw = {**payload, **kw}
            except ValidationError as e:
                if logger:
                    logger.info(
                        "Error while validating {0}. payload={1}, Error={2}".format(schema_key, payload, e.messages))
                error = errors['BadRequestError']
                res = {'message': e.messages, 'error': error['error'], 'status': error['status']}
                return Response(ErrorSchema().dumps(res), mimetype="application/json", status=error['status'])
            return f(*args, **kw)

        return wrapper

    return decorator