import types

from .common import get_database_connector, api_route
from .manage import create_app, create_api

# Initialize the flask app
app = create_app()

# Initialize the RESTful api
api = create_api(app)

# Initialize database engine and session
db_engine, db_Session = get_database_connector(logger=None, sql_database='MySQL')

# Adding the api to the api.route object
api.route = types.MethodType(api_route, api)

# import RESTful APIs
from app.apis import *
