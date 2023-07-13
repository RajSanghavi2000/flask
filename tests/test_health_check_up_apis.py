import pytest

from tests.fixtures import client_fixture, app_fixture
from app.common import APP_READINESS_API, APP_LIVENESS_API, APP_TERMINATION_API


@pytest.mark.run(order=9)
def test_health_check_apis(app_fixture, client_fixture):
    """This method is used to test api init task to create queues"""

    app_readiness_result = client_fixture.get(APP_READINESS_API)
    app_liveness_result = client_fixture.get(APP_LIVENESS_API)
    app_termination_result = client_fixture.get(APP_TERMINATION_API)

    assert app_readiness_result.status_code == 204
    assert app_liveness_result.status_code == 204
    assert app_termination_result.status_code == 204


