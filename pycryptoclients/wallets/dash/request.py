from requests.auth import HTTPBasicAuth

from pycryptoclients.request import BaseCCRequest
from pycryptoclients.utils import make_nonce


class DashRPCRequest(BaseCCRequest):

    def __init__(self, rpc_user, rpc_password, **kwargs):
        super(DashRPCRequest, self).__init__(**kwargs)
        self.method = 'POST'
        self.url = self.base_url
        self.auth = HTTPBasicAuth(rpc_user, rpc_password)
        self.headers['Content-Type'] = 'text/plain'
        self.json = {
            'method': self.api_method,
            'jsonrpc': '1.0',
            'id': str(make_nonce()),
            'params': []
        }


class GetInfoRequest(DashRPCRequest):
    api_method = 'getinfo'
