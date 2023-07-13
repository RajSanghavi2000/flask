from ...common.DataAccessLib.database.models import Person
from sqlalchemy.exc import IntegrityError

from app import app
from ...common import DuplicateEmailException, filter_orm_insert_result, dto_mapper
from .sample_mapper_schema import AddPersonInSQLMapperSchema, GetOrDeletePersonFromSQLMapperSchema, \
    UpdatePersonInSQLMapperSchema


def add_person_in_sql(session, person_dto, utc_timestamp):
    """This method is used to add person details in SQL database. It will raise IntegrityError for duplicate key"""

    mapper = dto_mapper(AddPersonInSQLMapperSchema, person_dto)
    try:
        data = Person(first_name=mapper.first_name, last_name=mapper.last_name, email=mapper.email,
                      phone=mapper.phone, created_at=utc_timestamp, created_by=mapper.created_by)
        session.add(data)
        session.flush()

        return filter_orm_insert_result(data.__dict__)
    except IntegrityError as e:
        app.logger.info("Duplicate email address {}".format(mapper.email))
        raise DuplicateEmailException


def get_person_from_sql(session, person_dto):
    """This method is used to fetch person details from the SQL database"""

    mapper = dto_mapper(GetOrDeletePersonFromSQLMapperSchema, person_dto)
    return session.query(Person).filter_by(id=mapper.id).first()


def update_person_in_sql(session, person_dto, modified_at):
    """This method is used to update the person details into the SQL database"""

    mapper = dto_mapper(UpdatePersonInSQLMapperSchema, person_dto)
    data = session.query(Person).filter_by(id=mapper.id).update(dict(phone=mapper.phone, modified_by=mapper.modified_by,
                                                                     modified_at=modified_at))
    return data


def delete_person_from_sql(session, person_dto):
    """This method is used to delete person details from the SQL database"""

    mapper = dto_mapper(GetOrDeletePersonFromSQLMapperSchema, person_dto)
    data = session.query(Person).filter_by(id=mapper.id).delete()

    return data
