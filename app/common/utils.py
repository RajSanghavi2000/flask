__all__ = ['filter_orm_insert_result', 'dto_mapper']


def filter_orm_insert_result(payload):
    if '_sa_instance_state' in payload:
        del payload['_sa_instance_state']

    return payload


def dto_mapper(schema_class, dto_object):
    return schema_class().load(dto_object.__dict__)

