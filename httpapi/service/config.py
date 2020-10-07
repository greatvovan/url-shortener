import os


DEBUG_API_PORT = int(os.getenv('DEBUG_API_PORT', '8080'))
LINK_TEMPLATE = os.getenv('LINK_TEMPLATE', f'http://localhost:{DEBUG_API_PORT}/{{}}')
URL_MAX_LENGTH = int(os.getenv('URL_MAX_LENGTH', '2000'))

TARANTOOL_HOST = os.getenv('TARANTOOL_HOST')
TARANTOOL_PORT = int(os.getenv('TARANTOOL_PORT', '3301'))

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
