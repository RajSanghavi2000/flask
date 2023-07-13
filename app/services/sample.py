import json

from DataAccessLib.database.connect import SessionHandler
from app import db_Session, app, message_broker_connection_pool, message_broker
from ..models.mysql.sample import add_person_in_sql, get_person_from_sql, update_person_in_sql, delete_person_from_sql
from ..common import PersonNotFoundException, QueueEnum, str_datetime as datetime_to_str, get_timestamp

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

        add_person_in_redis(self.person_dto, self.person_data.get('id'), self.utc_timestamp)

        message_broker.connection_pool_publish(message_broker_connection_pool,
                                               QueueEnum.SAMPLE_PERSON.value['exchange'],
                                               QueueEnum.SAMPLE_PERSON.value['routing_key'], json.dumps(self.person_data),
                                               delivery_mode=2)
        return self.person_data

    def get_person(self):
        """
        This method is used to handle fetch person data details operations.
        - Get person from Redis
        - If data not found in Redis then will use ``sync_person_data_into_the_redis()`` to sync the data

        :return: Person object
        """

        self.person_data = get_person_from_redis(self.person_dto)
        if not self.person_data:
            self.sync_person_data_into_the_redis()

        return self.person_data

    def update_person(self):
        """
        This method is used to handle person details operations
        - Update person in SQL
        - Sync person details into the Redis

        :return: Person object
        """

        with SessionHandler(db_Session) as session:
            data = update_person_in_sql(session, self.person_dto, self.utc_timestamp)
            session.commit()
        if not data:
            raise PersonNotFoundException

        self.sync_person_data_into_the_redis()
        return self.person_data

    def delete_person(self):
        """
        This method is used to handle delete person details operation
        - Delete from SQL database
        - If person details not found then raise Person not found exception
        - Else remove person details from redis
        """

        with SessionHandler(db_Session) as session:
            result = delete_person_from_sql(session, self.person_dto)
            session.commit()
        if not result:
            app.logger.info("Person {} not found while deleting the person details".format(self.person_dto.id))
            raise PersonNotFoundException

        delete_person_from_redis(self.person_dto)

    def sync_person_data_into_the_redis(self):
        """
        This method is used to sync person data into the redis
        - Fetch person data from SQL database
        - IF data found:
            - Add required field to person_dto
            - Add person data into the Redis
        - Else:
            - Raise Person no found exception

        :return: Person data
        """

        with SessionHandler(db_Session) as session:
            data = get_person_from_sql(session, self.person_dto)
        if not data:
            app.logger.info("Person {} not found while syncing person data into the redis".format(self.person_dto.id))
            raise PersonNotFoundException

        self.person_data = data.__dict__

        self.person_dto.id = self.person_data.get('id')
        self.person_dto.first_name = self.person_data.get("first_name")
        self.person_dto.last_name = self.person_data.get("last_name")
        self.person_dto.email = self.person_data.get("email")
        self.person_dto.phone = self.person_data.get("phone")
        self.person_dto.created_by = self.person_data.get("created_by")
        self.person_dto.modified_by = self.person_data.get("modified_by")

        add_person_in_redis(self.person_dto, self.person_dto.id,
                            datetime_to_str(self.person_data.get("created_at")),
                            datetime_to_str(self.person_data.get("modified_at")))

        return self.person_data
