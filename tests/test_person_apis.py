import pytest

from copy import deepcopy
from mock import patch

from tests.common.constants import *
from tests.common.utils import MockDb


@pytest.mark.run(order=10)
def test_set_person_header_validation(app_fixture, client_fixture):
    """This method is used test set person header validation"""

    response = client_fixture.post(sample_api, headers={})

    assert response.status_code == 400


@pytest.mark.run(order=11)
def test_set_person_first_name_body(app_fixture, client_fixture):
    """This method is used test set person json body first_name validation"""

    payload = deepcopy(set_person_payload)
    payload['first_name'] = ''
    response = client_fixture.post(sample_api, headers={'WT_USER_ID': 1}, json=payload)

    assert response.status_code == 400


@pytest.mark.run(order=12)
def test_set_person_last_name_body(app_fixture, client_fixture):
    """This method is used test set person json body last_name validation"""

    payload = deepcopy(set_person_payload)
    payload['last_name'] = 25
    response = client_fixture.post(sample_api, headers={'WT_USER_ID': 1}, json=payload)

    assert response.status_code == 400


@pytest.mark.run(order=13)
def test_set_person_email_body(app_fixture, client_fixture):
    """This method is used test set person json body email validation"""

    payload = deepcopy(set_person_payload)
    payload['email'] = ''
    response = client_fixture.post(sample_api, headers={'WT_USER_ID': 1}, json=payload)

    assert response.status_code == 400


@pytest.mark.run(order=14)
def test_set_person_phone_body(app_fixture, client_fixture):
    """This method is used test set person json body phone validation"""

    payload = deepcopy(set_person_payload)
    payload['phone'] = '256896'
    response = client_fixture.post(sample_api, headers={'WT_USER_ID': 1}, json=payload)

    assert response.status_code == 400


@pytest.mark.run(order=15)
def test_get_person_header_validation(app_fixture, client_fixture):
    """This method is used test get person header validation"""

    response = client_fixture.get('{0}?id={1}'.format(sample_api, 1), headers={})

    assert response.status_code == 400


@pytest.mark.run(order=16)
def test_get_person_arguments_validation(app_fixture, client_fixture):
    """This method is used test get person arguments validation"""

    response = client_fixture.get(sample_api, headers={'WT_USER_ID': 1})

    assert response.status_code == 400


@pytest.mark.run(order=17)
def test_update_person_header_validation(app_fixture, client_fixture):
    """This method is used test update person header validation"""

    response = client_fixture.put(sample_api, headers={})

    assert response.status_code == 400


@pytest.mark.run(order=18)
def test_update_person_json_body_phone_validation(app_fixture, client_fixture):
    """This method is used test update person json body phone validation"""

    response = client_fixture.put(sample_api, headers={'WT_USER_ID': 1}, json={'phone': '', 'id': 1})

    assert response.status_code == 400


@pytest.mark.run(order=19)
def test_update_person_json_body_ide_validation(app_fixture, client_fixture):
    """This method is used test update person json body id validation"""

    response = client_fixture.put(sample_api, headers={'WT_USER_ID': 1}, json={'phone': '5252858578', 'id': ''})

    assert response.status_code == 400


@pytest.mark.run(order=20)
def test_delete_person_header_validation(app_fixture, client_fixture):
    """This method is used test delete person header validation"""

    response = client_fixture.delete(sample_api, headers={})

    assert response.status_code == 400


@pytest.mark.run(order=21)
def test_delete_person_json_body_id_validation(app_fixture, client_fixture):
    """This method is used test delete person json body id validation"""

    response = client_fixture.delete(sample_api, headers={'WT_USER_ID': 1}, json={'id': ''})

    assert response.status_code == 400


@pytest.mark.run(order=22)
@patch('app.services.sample.add_person_in_sql', return_value=add_person_in_sql_mock)
@patch('app.services.sample.add_person_in_redis', return_value=None)
@patch('DataAccessLib.database.connect.connect', return_value=MockDb)
@patch('DataAccessLib.database.connect.close', return_value=None)
@patch('MessageBrokerLib.broker.RabbitMQPika.connection_pool_publish', return_value=None)
def test_add_person(mock_add_person_sql, mock_add_person_redis, mock_db, mock_db_close, app_fixture,
                    client_fixture):
    """This method is used to test add person API"""

    payload = deepcopy(set_person_payload)
    response = client_fixture.post(sample_api, headers={'WT_USER_ID': 1}, json=payload)

    assert response.status_code == 201
    assert response.json == person_expected_response


@pytest.mark.run(order=23)
@patch('app.services.sample.get_person_from_redis', return_value=get_person_from_redis_mock)
def test_get_person_from_redis(mock_get_person_redis, app_fixture, client_fixture):
    """This method is used to test add person API"""

    payload = deepcopy(set_person_payload)
    response = client_fixture.get('{0}?id={1}'.format(sample_api, 7), headers={'WT_USER_ID': 1})

    assert response.status_code == 200
    assert response.json == person_expected_response


@pytest.mark.run(order=24)
@patch('app.services.sample.get_person_from_redis', return_value=None)
@patch('DataAccessLib.database.connect.connect', return_value=MockDb)
@patch('DataAccessLib.database.connect.close', return_value=None)
@patch('app.services.sample.get_person_from_sql', return_value=get_person_from_sql)
@patch('app.services.sample.add_person_in_redis', return_value=None)
def test_get_person_from_sql_and_redis(mock_get_person_redis, mock_db_conn, mock_db_close, mock_get_person_sql,
                                       mock_add_person_redis, app_fixture, client_fixture):
    """This method is used to test add person API"""

    payload = deepcopy(set_person_payload)
    response = client_fixture.get('{0}?id={1}'.format(sample_api, 7), headers={'WT_USER_ID': 1})

    assert response.status_code == 200
    assert response.json == person_expected_response


@pytest.mark.run(order=25)
@patch('app.services.sample.get_person_from_redis', return_value=None)
@patch('DataAccessLib.database.connect.connect', return_value=MockDb)
@patch('DataAccessLib.database.connect.close', return_value=None)
@patch('app.services.sample.get_person_from_sql', return_value=None)
@patch('app.services.sample.add_person_in_redis', return_value=None)
def test_get_person_not_found_exception(mock_get_person_redis, mock_db_conn, mock_db_close, mock_get_person_sql,
                                       mock_add_person_redis, app_fixture, client_fixture):
    """This method is used to test add person API"""

    payload = deepcopy(set_person_payload)
    response = client_fixture.get('{0}?id={1}'.format(sample_api, 7), headers={'WT_USER_ID': 1})

    assert response.status_code == 404


@pytest.mark.run(order=26)
@patch('DataAccessLib.database.connect.connect', return_value=MockDb)
@patch('DataAccessLib.database.connect.close', return_value=None)
@patch('app.services.sample.update_person_in_sql', return_value=True)
@patch('app.services.sample.get_person_from_sql', return_value=get_person_from_sql)
@patch('app.services.sample.add_person_in_redis', return_value=None)
def test_update_person(mock_db_conn, mock_db_close, mock_update_person_sql, mock_get_person_sql,
                       mock_add_person_redis, app_fixture, client_fixture):
    """This method is used to test add person API"""

    payload = deepcopy(set_person_payload)
    response = client_fixture.put(sample_api, headers={'WT_USER_ID': 1}, json=update_person_payload)

    assert response.status_code == 200
    assert response.json == person_expected_response


@pytest.mark.run(order=27)
@patch('DataAccessLib.database.connect.connect', return_value=MockDb)
@patch('DataAccessLib.database.connect.close', return_value=None)
@patch('app.services.sample.update_person_in_sql', return_value=False)
def test_update_person_not_found_exception(mock_db_conn, mock_db_close, mock_update_person_sql, app_fixture, client_fixture):
    """This method is used to test add person API"""

    payload = deepcopy(set_person_payload)
    response = client_fixture.put(sample_api, headers={'WT_USER_ID': 1}, json=update_person_payload)

    assert response.status_code == 404


@pytest.mark.run(order=28)
@patch('DataAccessLib.database.connect.connect', return_value=MockDb)
@patch('DataAccessLib.database.connect.close', return_value=None)
@patch('app.services.sample.delete_person_from_sql', return_value=True)
@patch('app.services.sample.delete_person_from_redis', return_value=True)
def test_delete_person(mock_db_conn, mock_db_close, mock_delete_person_from_sql, mock_delete_person_from_redis,
                       app_fixture, client_fixture):
    """This method is used to test add person API"""

    payload = deepcopy(set_person_payload)
    response = client_fixture.delete(sample_api, headers={'WT_USER_ID': 1}, json=delete_person_payload)

    assert response.status_code == 200
    assert response.json == delete_person_expected_response


@pytest.mark.run(order=29)
@patch('DataAccessLib.database.connect.connect', return_value=MockDb)
@patch('DataAccessLib.database.connect.close', return_value=None)
@patch('app.services.sample.delete_person_from_sql', return_value=False)
@patch('app.services.sample.delete_person_from_redis', return_value=True)
def test_delete_person_not_found_exception(mock_db_conn, mock_db_close, mock_delete_person_from_sql, mock_delete_person_from_redis,
                                           app_fixture, client_fixture):
    """This method is used to test add person API"""

    payload = deepcopy(set_person_payload)
    response = client_fixture.delete(sample_api, headers={'WT_USER_ID': 1}, json=delete_person_payload)

    assert response.status_code == 404
