import os

from app.common import SAMPLE_API
from tests.common.utils import dict2obj


graylog_expected_result = '<Logger app.manage (INFO)>'
mysq_orm_engine_expected_result = "Engine(mysql+pymysql://{user}:***@{host}/{db})".format(user=os.environ['MYSQL_DATABASE_USER'],
                                                                                          host=os.environ['MYSQL_DATABASE_HOST'],
                                                                                          db=os.environ['MYSQL_DATABASE_DB'])

message_broker_expected_result = "<class 'MessageBrokerLib.broker.rabbitmq.rabbitmq_pika.rabbitmq_pika.RabbitMQPika'>"
rabbitmq_connection_pool_expected_result = "<pika_pool.QueuedPool object at"
api_route_expected_result = "<bound method api_route of <flask_restful.Api object at"
sample_api = "api{}".format(SAMPLE_API)


# Person

set_person_payload = {"first_name": "xyz", "last_name": "abx", "email": "anc.bnv@marutistech.com",
                      "phone": "6565656565"}

add_person_in_sql_mock = {'first_name': 'xyz', 'last_name': 'abc', 'email': 'xyz@abc.com',
                          'phone': '6565656565', 'created_at': '2021-03-04 09:20:17.477031',
                          'created_by': 1, 'id': 7}
person_expected_response = {**add_person_in_sql_mock, **{"modified_at": None, "modified_by": None}}

delete_person_payload = {'id': 7}
get_person_from_redis_mock = {'phone': '6565656565', 'created_by': 1, 'modified_by': None,
                              'email': 'xyz@abc.com', 'first_name': 'xyz',
                              'last_name': 'abc', 'created_at': '2021-03-04 09:20:17.477031', 'modified_at': None, 'id': 7}

get_person_from_sql = dict2obj({'phone': '6565656565', 'last_name': 'abc', 'id': 7, 'modified_at': None,
                                'created_at': "2021-03-04 09:20:17.477031", 'email': 'xyz@abc.com',
                                'first_name': 'xyz', 'modified_by': None, 'created_by': 1})

update_person_payload = {'id': 7, 'phone': '6565656565', 'meta': {"first_name": "xyz", "last_name": "abc",
                                                                  "email": "xyz@abc.com"}}

delete_person_expected_response = {"ok": True}
