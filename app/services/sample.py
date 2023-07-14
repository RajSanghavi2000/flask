from app import db_Session, app
from ..models.mysql.sample import add_person_in_sql, get_person_from_sql, update_person_in_sql, delete_person_from_sql
from ..common import PersonNotFoundException, str_datetime as datetime_to_str, get_timestamp, SessionHandler

__all__ = ['PersonsManagementService']


class PersonsManagementService:
    """
    This class is used to manage the CRUD operations for the person. It's have below methods.
    - add_person(): Add person details in database
    - get_person(): Get person details
    - update_person(): Update the person details
    - delete_person(): Delete the person from the database
    - prepare_response_payload(): Prepare response payload

    """

    def __init__(self, person_dto):
        self.current_utc_timestamp = get_timestamp()
        self.person_dto = person_dto
        self.utc_timestamp = datetime_to_str(self.current_utc_timestamp)
        self.person_data = None

    def add_person(self):
        """
        This method is used to handle add person details operation.
        - Add person in SQL Database

        :return: Person object
        """

        with SessionHandler(db_Session) as session:
            self.person_data = add_person_in_sql(session, self.person_dto, self.utc_timestamp)
            session.commit()
        return self.person_data

    def get_person(self):
        """
        This method is used to handle fetch person data details operations.
        - Get person from SQL

        :return: Person object
        """

        with SessionHandler(db_Session) as session:
            data = get_person_from_sql(session, self.person_dto)
        if not data:
            app.logger.info(
                "Person {} not found into the SQL".format(self.person_dto.id))
            raise PersonNotFoundException

        self.person_data = data.__dict__

        self.person_dto.id = self.person_data.get('id')
        self.person_dto.first_name = self.person_data.get("first_name")
        self.person_dto.last_name = self.person_data.get("last_name")
        self.person_dto.email = self.person_data.get("email")
        self.person_dto.phone = self.person_data.get("phone")
        self.person_dto.created_by = self.person_data.get("created_by")
        self.person_dto.modified_by = self.person_data.get("modified_by")

        return self.person_data

    def update_person(self):
        """
        This method is used to handle person details operations
        - Update person in SQL

        :return: Person object
        """

        with SessionHandler(db_Session) as session:
            data = update_person_in_sql(session, self.person_dto, self.utc_timestamp)
            session.commit()
        if not data:
            raise PersonNotFoundException
        return self.person_dto

    def delete_person(self):
        """
        This method is used to handle delete person details operation
        - Delete from SQL database
        - If person details not found then raise Person not found exception
        """

        with SessionHandler(db_Session) as session:
            result = delete_person_from_sql(session, self.person_dto)
            session.commit()
        if not result:
            app.logger.info("Person {} not found while deleting the person details".format(self.person_dto.id))
            raise PersonNotFoundException
