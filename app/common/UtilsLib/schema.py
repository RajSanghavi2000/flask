from marshmallow import Schema, fields, EXCLUDE, validate, post_dump


__all__ = ['ErrorSchema', 'DefaultResponseSchema', 'HeaderSchema']


class ErrorSchema(Schema):
    ok = fields.Boolean(default=False)
    error = fields.String(default='INTERNAL_SERVER')
    message = fields.Raw()
    status = fields.Integer(default=500)


class DefaultResponseSchema(Schema):
    ok = fields.Boolean(default=True)


class HeaderSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    WT_USER_ID = fields.Integer(required=True, allow_none=False, validate=validate.Range(min=1))
    WT_CORRELATION_ID = fields.String(required=True, allow_none=False, validate=validate.Length(min=1))

    @post_dump(pass_many=True)
    def change_key(self, data, many, **kwargs):
        return {"user_id": data.get('WT_USER_ID')}
