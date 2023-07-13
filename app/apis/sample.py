from flask import Response
from flask_restful import Resource

from app import api, app
from ..common import (SAMPLE_API, UserIdHeaderSchema,
                      GetPersonArgumentsSchema, SetPersonRequestSchema, UpdatePersonRequestSchema,
                      DeletePersonRequestSchema, PersonResponseSchema, DefaultResponseSchema, StatusCodeEnum,
                      validate_api_schema, AddPersonDTO, GetOrDeletePersonDTO, UpdatePersonDTO, SchemaKeysEnum,)
from ..services import PersonsManagementService

__all__ = ['PersonsManagement']


@api.route(SAMPLE_API)
class PersonsManagement(Resource):

    @validate_api_schema(schema_key=SchemaKeysEnum.HEADER.value, schema_class=UserIdHeaderSchema, logger=app.logger)
    @validate_api_schema(schema_key=SchemaKeysEnum.ARGUMENTS.value, schema_class=GetPersonArgumentsSchema, logger=app.logger)
    def get(self, **kwargs):
        """
        Get endpoint to fetch person details.
        Required arguments:
            id: Unique id assigned to every person

        :return: Person object
        """

        service = PersonsManagementService(GetOrDeletePersonDTO(**kwargs))
        response = service.get_person()

        return Response(PersonResponseSchema().dumps(response), mimetype="application/json", status=StatusCodeEnum.SUCCESS.value)

    @validate_api_schema(schema_key=SchemaKeysEnum.HEADER.value, schema_class=UserIdHeaderSchema, logger=app.logger)
    @validate_api_schema(schema_key=SchemaKeysEnum.JSON.value, schema_class=SetPersonRequestSchema, logger=app.logger)
    def post(self, **kwargs):
        """
        Post endpoint to add person details into the database
        Required JSON body:
            first_name: First name of the person
            last_name: Last name of the person
            email: Email address of the person
            phone: Phone number of the person

        :return: Person object
        """

        service = PersonsManagementService(AddPersonDTO(**kwargs))

        response = service.add_person()

        return Response(PersonResponseSchema().dumps(response), mimetype="application/json", status=StatusCodeEnum.CREATED_RESPONSE.value)

    @validate_api_schema(schema_key=SchemaKeysEnum.HEADER.value, schema_class=UserIdHeaderSchema, logger=app.logger)
    @validate_api_schema(schema_key=SchemaKeysEnum.JSON.value, schema_class=UpdatePersonRequestSchema, logger=app.logger)
    def put(self, **kwargs):
        """
        Put endpoint to update the person details
        Required JSON body:
            id: Unique id assigned to every person
            phone: Phone number of the person
            meta:
                first_name: First name of the person
                last_name: Last name of the person
                email: Email address of the person

        :return: Person object
        """

        service = PersonsManagementService(UpdatePersonDTO(**kwargs))

        response = service.update_person()

        return Response(PersonResponseSchema().dumps(response), mimetype="application/json", status=StatusCodeEnum.SUCCESS.value)

    @validate_api_schema(schema_key=SchemaKeysEnum.HEADER.value, schema_class=UserIdHeaderSchema, logger=app.logger)
    @validate_api_schema(schema_key=SchemaKeysEnum.JSON.value, schema_class=DeletePersonRequestSchema, logger=app.logger)
    def delete(self, **kwargs):
        """
        Delete endpoint to delete the person details
        Required JSON body:
            id: Unique id assigned to every person

        :return: Default response true
        """

        service = PersonsManagementService(GetOrDeletePersonDTO(**kwargs))

        service.delete_person()

        return Response(DefaultResponseSchema().dumps(None), mimetype="application/json", status=StatusCodeEnum.SUCCESS.value)
