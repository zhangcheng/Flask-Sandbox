#-*- coding: utf-8 -*-


import time

from bson.objectid import ObjectId
from datetime import datetime, timedelta
from flask.ext.mongokit import Document
from hashlib import sha512
from uuid import uuid4


class TimestampGenerator(object):
    """Callable Timestamp Generator that returns a UNIX time integer.

    **Kwargs:**

    * *seconds:* A integer indicating how many seconds in the future the
      timestamp should be. *Default 0*

    *Returns int*
    """
    def __init__(self, seconds=0):
        self.seconds = seconds

    def __call__(self):
        return int(time.time()) + self.seconds


class KeyGenerator(object):
    """Callable Key Generator that returns a random keystring.

    **Args:**

    * *length:* A integer indicating how long the key should be.

    *Returns str*
    """
    def __init__(self, length):
        self.length = length

    def __call__(self):
        return sha512(uuid4().hex).hexdigest()[0:self.length]


class AccessToken(Document):
    """Stores access token data.

    **Args:**

    **Kwargs:**

    * *token:* A string representing the access key token. *Default 10
      character random string*
    * *expire:* A positive integer timestamp representing the access token's
      expiration time.

    """
    __collection__ = 'access_token'
    structure = {
        'token': unicode,
        'user_id': ObjectId,
        'issued_at': datetime,
        'expire_at': datetime,
    }
    required_fields = ['token', 'issued_at', 'expire_at']
    default_values = {'issued_at': datetime.utcnow(), 'expire_at': datetime.utcnow() + timedelta(seconds=3600)}
    use_dot_notation = True


class User(Document):
    __collection__ = 'user'
    structure = {
        'device_id': unicode,
        'services': {
            unicode: dict
        }
    }
    use_dot_notation = True
    use_schemaless = True
