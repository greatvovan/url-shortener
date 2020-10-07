import os


TARANTOOL_HOST = os.getenv('TARANTOOL_HOST', 'localhost')
TARANTOOL_PORT = int(os.getenv('TARANTOOL_PORT', '3301'))

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
