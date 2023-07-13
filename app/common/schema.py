from marshmallow import Schema, fields, EXCLUDE, validate


__all__ = ['UserIdHeaderSchema', 'GetPersonArgumentsSchema', 'SetPersonRequestSchema',
           'UpdatePersonRequestSchema', 'DeletePersonRequestSchema', 'PersonResponseSchema']


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
