from dataclasses import dataclass
from marshmallow import Schema, fields, post_load, EXCLUDE

__all__ = ['AddPersonInSQLMapperSchema', 'GetOrDeletePersonFromSQLMapperSchema', 'UpdatePersonInSQLMapperSchema']


@dataclass
class AddPersonInSQLMapper:
    first_name: str
    last_name: str
    phone: str
    email: str
    created_by: int


class AddPersonInSQLMapperSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    phone = fields.String(required=True)
    email = fields.String(required=True)
    created_by = fields.Integer(required=True, data_key='WT_USER_ID')

    @post_load
    def make_obj(self, data, **kwargs):
        return AddPersonInSQLMapper(**data)


@dataclass
class GetOrDeletePersonFromSQLMapper:
    id: int


class GetOrDeletePersonFromSQLMapperSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(required=True)

    @post_load
    def make_obj(self, data, **kwargs):
        return GetOrDeletePersonFromSQLMapper(**data)


@dataclass
class UpdatePersonInSQLMapper:
    id: int
    phone: str
    modified_by: int
    email: str
    first_name: str
    last_name: str


class UpdatePersonInSQLMapperSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(required=True)
    phone = fields.String(required=True)
    modified_by = fields.Integer(required=True, data_key='WT_USER_ID')
    email = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)

    @post_load
    def make_obj(self, data, **kwargs):
        return UpdatePersonInSQLMapper(**data)
