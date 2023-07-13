import json


class MockDb:
    @staticmethod
    def commit():
        pass


class Obj:
    def __init__(self, payload):
        self.__dict__.update(payload)


def dict2obj(payload):
    """using json.loads method and passing json.dumps method and custom object hook as arguments to convert dictionary
    into the object"""

    return json.loads(json.dumps(payload), object_hook=Obj)
