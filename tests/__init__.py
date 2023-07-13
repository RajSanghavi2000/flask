import os

os.environ['ENVIRONMENT'] = "DEV"
os.environ['DEBUG'] = "0"
os.environ['TESTING'] = "0"
os.environ['MICRO_SERVICE_PORT'] = "5111"
os.environ['PRODUCT_NAME'] = "WOTNOT"

os.environ['ENABLE_GRAYLOG'] = "0"
os.environ['GRAYLOG_HOST'] = "127.0.0.1"
os.environ['GRAYLOG_PORT'] = "9000"

os.environ['REDIS_CLUSTER_HOST'] = "127.0.0.1"
os.environ['REDIS_CLUSTER_PORT'] = "6379"
os.environ['REDIS_DATABASE'] = "0"
os.environ['REDIS_PASSWORD'] = ""

os.environ['MYSQL_DATABASE_USER'] = "xyz"
os.environ['MYSQL_DATABASE_PASSWORD'] = "xyz"
os.environ['MYSQL_DATABASE_HOST'] = "127.0.0.1"
os.environ['MYSQL_DATABASE_DB'] = "xyz"
os.environ['MYSQL_DATABASE_CONNECTION_POOL_SIZE'] = "10"
os.environ['MYSQL_DATABASE_CONNECTION_POOL_MAX_OVERFLOW_SIZE'] = "10"

os.environ['SERVER_THREAD_POOL'] = "30"
os.environ['SERVER_SHUTDOWN_TIMEOUT'] = "1"

os.environ['RABBIT_MQ_HOST'] = "127.0.0.1"
os.environ['RABBIT_MQ_PORT'] = "5672"
os.environ['RABBIT_MQ_V_HOST'] = "%2f"
os.environ['RABBIT_MQ_HEARTBEAT'] = "0"
os.environ['RABBIT_MQ_USERNAME'] = "xyz"
os.environ['RABBIT_MQ_PASSWORD'] = "xyz"
os.environ['PIKA_POOL_MAXIMUM_CONNECTION_LIMIT'] = "1"
os.environ['PIKA_POOL_MAXIMUM_CONNECTION_OVERFLOW_LIMIT'] = "10"
os.environ['PIKA_POOL_MAXIMUM_CONNECTION_ACQUIRE_TIME'] = "9"
os.environ['PIKA_POOL_CONNECTION_STATE_TIME_DURATION'] = "3600"
