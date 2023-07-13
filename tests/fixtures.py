import pytest
from mock import patch


from app import app, api, db_engine, db_Session, redis_instance, message_broker, message_broker_connection_pool


@pytest.fixture
def app_fixture():
    yield app


@pytest.fixture
def api_fixture():
    yield api


@pytest.fixture
def db_engine_fixture():
    yield db_engine


@pytest.fixture
def db_session_fixture():
    yield db_Session


@pytest.fixture
def redis_instance_fixture():
    yield redis_instance


@pytest.fixture
def message_broker_fixture():
    yield message_broker


@pytest.fixture
def message_broker_connection_pool_fixture():
    yield message_broker_connection_pool


@pytest.fixture
def client_fixture(app_fixture):
    return app_fixture.test_client()


