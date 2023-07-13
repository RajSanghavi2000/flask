import pytest
import os
import re

from builtins import int
from distutils.util import strtobool


from tests.fixtures import (app_fixture, api_fixture, db_engine_fixture, db_session_fixture)
from tests.common.constants import (graylog_expected_result, mysq_orm_engine_expected_result,
                                    api_route_expected_result)
from ..app.common import configure_logging_log_file, configure_graylog


@pytest.mark.run(order=1)
def test_config(app_fixture):
    """This method is used to test app config"""

    assert app_fixture.config['ENVIRONMENT'] == os.environ.get("ENVIRONMENT")
    assert app_fixture.config['DEBUG'] == strtobool(os.environ.get("DEBUG", "0"))
    assert app_fixture.config['TESTING'] == strtobool(os.environ.get("TESTING", "0"))
    assert app_fixture.config['PORT'] == int(os.environ.get("MICRO_SERVICE_PORT"))
    assert app_fixture.config['PRODUCT_NAME'] == os.environ.get("PRODUCT_NAME")
    assert app_fixture.config['SERVER_THREAD_POOL'] == int(os.environ.get("SERVER_THREAD_POOL"))
    assert app_fixture.config['SERVER_SHUTDOWN_TIMEOUT'] == int(os.environ.get("SERVER_SHUTDOWN_TIMEOUT"))

    assert app_fixture.config['ENABLE_GRAYLOG'] == int(os.environ.get("ENABLE_GRAYLOG"))
    assert app_fixture.config['GRAYLOG_HOST'] == os.environ.get("GRAYLOG_HOST")
    assert app_fixture.config['GRAYLOG_PORT'] == int(os.environ.get("GRAYLOG_PORT"))


@pytest.mark.run(order=2)
def test_local_logs(app_fixture):
    """This method is used to test ``configure_logging_log_file()`` method"""

    file_path = os.path.abspath(os.path.join(__file__, '..', '..', 'data', 'logs', 'log'))
    folder_path = os.path.abspath(os.path.join(__file__, '..', '..', 'data', 'logs'))
    if os.path.exists(file_path):
        os.remove(file_path)

    configure_logging_log_file(app_fixture, folder_path, file_path, 'midnight', 1, 1825)

    result = True if os.path.exists(file_path) else False

    assert result == True


@pytest.mark.run(order=3)
def test_gray_logs(app_fixture):
    """This method is used to test ``configure_graylog()`` method"""

    configure_graylog(app_fixture, 'microservice-template')

    assert str(app_fixture.logger) == graylog_expected_result


@pytest.mark.run(order=5)
def test_mysql_orm_connection(db_engine_fixture, db_session_fixture):
    """This method is used to test ORM connection"""

    assert str(db_engine_fixture) == mysq_orm_engine_expected_result
    assert str(db_session_fixture.kw.get("bind")) == mysq_orm_engine_expected_result


@pytest.mark.run(order=8)
def test_api_route(api_fixture):
    """This method is used to test api route"""

    assert re.match(api_route_expected_result, str(api_fixture.route)) is not None


