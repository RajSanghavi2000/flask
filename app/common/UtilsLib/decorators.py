import os
from enum import Enum

import jwt
from functools import wraps
from flask import Response, request, current_app
from marshmallow.exceptions import ValidationError
from jwt.exceptions import PyJWTError, DecodeError, InvalidSignatureError
from dataclasses import dataclass, is_dataclass
from UtilsLib.error import errors
from UtilsLib.utility import get_request_payload, prepare_error_response, parse_response, get_all_nested_error_messages
from UtilsLib.schema import ErrorSchema

__all__ = ['api_route', 'validate_api_schema', 'nested_dataclass', 'validate_access_token',
           'validate_api_request_schema', 'validate_api_schemav2', 'extend_enum']


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


def validate_api_request_schema(schema_key, schema_class, logger=None):
    """
    This method is used to validate api request headers, arguments and body of type json. It's using marshmallow to
    validate the schema. If request schema is invalid then it returns custom validation errors respectively.

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

                messages = e.messages

                exceptions = prepare_error_response(messages)

                return parse_response(exceptions)

            return f(*args, **kw)

        return wrapper

    return decorator


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


def validate_access_token(token=None, logger=None):
    """
    Validate jwt token received in the request
    :param token: Authorization token to validate
    :param logger: app logger object. Default None
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                _token = token if token else request.headers.get('AUTHORIZATION', '')
                _token = _token.replace('Bearer ', '')
                # Verify JWT in the request
                payload = jwt.decode(jwt=_token, key=os.environ.get('JWT_SECRET_KEY'),
                                     algorithms=os.environ.get('JWT_ALGORITHM', "HS256"))
                kwargs = {**kwargs, **payload}
            except (InvalidSignatureError, DecodeError, PyJWTError):
                if not request.headers.get('AUTHORIZATION', '').replace('Bearer ', '') == \
                       current_app.config['SCHEDULER_SECRET']:
                    # Backdoor authentication access
                    if logger:
                        logger.exception("Invalid JWT Access Token Received")
                    error = errors['JWtSignatureException']
                    return Response(ErrorSchema().dumps(error), mimetype="application/json", status=error['status'])
            except Exception as e:
                if logger:
                    logger.exception("Error while validating the access token: {}".format(str(e)))
                raise Exception from e
            return f(*args, **kwargs)

        return wrapper

    return decorator


def validate_api_schemav2(schema_key, schema_class, logger=None):
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
                res = {'message': get_all_nested_error_messages(e.messages)[0], 'error': error['error'], 'status': error['status']}
                return Response(ErrorSchema().dumps(res), mimetype="application/json", status=error['status'])
            return f(*args, **kw)

        return wrapper

    return decorator


def extend_enum(inherited_enum):
    def wrapper(added_enum):
        joined = {}
        for item in inherited_enum:
            joined[item.name] = item.value
        for item in added_enum:
            joined[item.name] = item.value
        return Enum(added_enum.__name__, joined)
    return wrapper
