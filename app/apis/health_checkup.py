from app import app

from ..common.constants import APP_READINESS_API, APP_LIVENESS_API, APP_TERMINATION_API

__all__ = ['service_status']


@app.route(APP_READINESS_API)
@app.route(APP_LIVENESS_API)
@app.route(APP_TERMINATION_API)
def service_status():
    return '', 204
