from .decorators import nested_dataclass

__all__ = ['AddPersonDTO', 'GetOrDeletePersonDTO', 'UpdatePersonDTO']


@nested_dataclass
class AddPersonDTO:
    first_name: str
    last_name: str
    phone: str
    email: str
    WT_USER_ID: str


@nested_dataclass
class GetOrDeletePersonDTO:
    WT_USER_ID: str
    id: int


@nested_dataclass
class UpdateMeta:
    first_name: str
    last_name: str
    email: str


@nested_dataclass
class UpdatePersonDTO:
    id : int
    phone: str
    WT_USER_ID: str
    meta: UpdateMeta


