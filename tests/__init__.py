import os

os.environ['ENVIRONMENT'] = "DEV"
os.environ['DEBUG'] = "0"
os.environ['TESTING'] = "0"
os.environ['MICRO_SERVICE_PORT'] = "5111"
os.environ['PRODUCT_NAME'] = "WOTNOT"

os.environ['ENABLE_GRAYLOG'] = "0"
os.environ['GRAYLOG_HOST'] = "127.0.0.1"
os.environ['GRAYLOG_PORT'] = "9000"

os.environ['MYSQL_DATABASE_USER'] = "xyz"
os.environ['MYSQL_DATABASE_PASSWORD'] = "xyz"
os.environ['MYSQL_DATABASE_HOST'] = "127.0.0.1"
os.environ['MYSQL_DATABASE_DB'] = "xyz"
os.environ['MYSQL_DATABASE_CONNECTION_POOL_SIZE'] = "10"
os.environ['MYSQL_DATABASE_CONNECTION_POOL_MAX_OVERFLOW_SIZE'] = "10"

os.environ['SERVER_THREAD_POOL'] = "30"
os.environ['SERVER_SHUTDOWN_TIMEOUT'] = "1"

