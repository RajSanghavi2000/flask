from functools import wraps
from flask import Response
from marshmallow.exceptions import ValidationError
from error import errors
from utils import get_request_payload
from schema import ErrorSchema

__all__ = ['api_route', 'validate_api_schema']


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