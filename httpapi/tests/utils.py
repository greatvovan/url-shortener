import uuid


def get_long_url(length: int):
    return 'http://domain.com/' + 'long-long/' * ((length // 10) - 2)    # Approximate


def get_random_string():
    return str(uuid.uuid4())
