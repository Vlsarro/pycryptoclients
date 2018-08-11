import json
import hmac
import hashlib
from requests import PreparedRequest
from requests.auth import AuthBase

from pycryptoclients.utils import make_nonce, ENCODING


class HmacAuth(AuthBase):

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def __call__(self, request: PreparedRequest):
        data = json.loads(request.body)
        data['nonce'] = make_nonce()
        signdata = json.dumps(data)
        sign = hmac.new(self.api_secret, bytearray(signdata, encoding=ENCODING), hashlib.sha512).hexdigest()
        request.headers.update({
            'Key': self.api_key,
            'Sign': sign
        })
        request.body = signdata
        return request
