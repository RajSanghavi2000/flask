__all__ = ['DuplicateEmailException', 'PersonNotFoundException', "InvalidSQLDataBase"]


class DuplicateEmailException(Exception):
    pass


class PersonNotFoundException(Exception):
    pass


class InvalidSQLDataBase(Exception):
    def __init__(self, msg):
        self.msg = msg
