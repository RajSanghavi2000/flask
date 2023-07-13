from marshmallow import Schema, fields, EXCLUDE, validate, post_dump


__all__ = ['ErrorSchema', 'DefaultResponseSchema', 'HeaderSchema', 'UserIdHeaderSchema', 'GetPersonArgumentsSchema',
           'SetPersonRequestSchema', 'UpdatePersonRequestSchema', 'DeletePersonRequestSchema', 'PersonResponseSchema',
           'ErrorSchema']


class UserIdHeaderSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    WT_USER_ID = fields.Raw(required=True, allow_none=False)


class GetPersonArgumentsSchema(Schema):
    id = fields.Integer(required=True, allow_none=False)


class SetPersonRequestSchema(Schema):
    first_name = fields.String(required=True, allow_none=False, validate=validate.Length(min=1, max=50))
    last_name = fields.String(required=True, allow_none=False, validate=validate.Length(min=1, max=50))
    email = fields.String(required=True, validate=validate.Email())
    phone = fields.String(required=True, validate=validate.Length(equal=10))


class UpdatePersonMetaSchema(Schema):
    first_name = fields.String(required=True, allow_none=False, validate=validate.Length(min=1, max=50))
    last_name = fields.String(required=True, allow_none=False, validate=validate.Length(min=1, max=50))
    email = fields.String(required=True, validate=validate.Email())


class UpdatePersonRequestSchema(Schema):
    id = fields.Integer(required=True, allow_none=False)
    phone = fields.String(required=True, validate=validate.Length(equal=10))
    meta = fields.Nested(UpdatePersonMetaSchema, required=True, allow_none=False)


class DeletePersonRequestSchema(Schema):
    id = fields.Integer(required=True, allow_none=False)


class PersonResponseSchema(Schema):
    id = fields.Integer(required=True, allow_none=False)
    first_name = fields.String(required=True, allow_none=False, validate=validate.Length(min=1, max=50))
    last_name = fields.String(required=True, allow_none=False, validate=validate.Length(min=1, max=50))
    email = fields.String(required=True, validate=validate.Email())
    phone = fields.String(required=True, validate=validate.Length(equal=10))
    created_at = fields.String(required=True, allow_none=False)
    created_by = fields.Integer(required=True, allow_none=False)
    modified_at = fields.String(allow_none=True, default=None)
    modified_by = fields.Integer(allow_none=True, default=None)


class ErrorSchema(Schema):
    ok = fields.Boolean(default=False)
    error = fields.String(default='INTERNAL_SERVER')
    message = fields.Raw()
    status = fields.Integer(default=500)


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
