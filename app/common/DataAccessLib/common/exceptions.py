__all__ = ["InvalidSQLDataBase"]


class InvalidSQLDataBase(Exception):
    def __init__(self, msg):
        self.msg = msg
