import types

from DataAccessLib.database.connect import get_database_connector

from UtilsLib import api_route
from .manage import create_app, create_api, app_init

# Initialize the flask app
app = create_app()

# Initialize the RESTful api
api = create_api(app)

# Initialize redis instance
redis_instance = CacheHandlerFactory('redis').get_instance()

# Initialize database engine and session
db_engine, db_Session = get_database_connector(cache_conn=redis_instance, logger=None, sql_database='MySQL')

# Initialize RabbitMQ Connection
message_broker = MessageBroker.broker(broker="RabbitMQ", client="Pika")
message_broker_connection_pool = message_broker.connection_pool()

# Adding the api to the api.route object
api.route = types.MethodType(api_route, api)


# Init APP task
def app_init_task():
    app_init(message_broker, message_broker_connection_pool)


# import RESTful APIs
from app.apis import *
