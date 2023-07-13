from enum import Enum

__all__ = ["DatabaseUrlEnum", "DatabaseEnum", "VariableFormatEnum"]


class DatabaseUrlEnum(Enum):
    MYSQL = "mysql+pymysql://{user}:{password}@{host}/{database}"


class DatabaseEnum(Enum):
    MYSQL = "MySQL"


class VariableFormatEnum(Enum):
    NAME = "name"
    EMAIL = "email"
    PHONE = "phone"
    NUMBER = "number"
    TEXT = "text"
    DATE = "date"
    REGEX = "regex"
    BOOLEAN = "boolean"

