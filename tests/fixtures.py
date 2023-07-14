import pytest


from app import app, api, db_engine, db_Session


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
def client_fixture(app_fixture):
    return app_fixture.test_client()
