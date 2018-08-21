from requests.auth import HTTPBasicAuth

from pycryptoclients.request import BaseCCRequest
from pycryptoclients.utils import make_nonce


class DashRPCRequest(BaseCCRequest):

    def __init__(self, rpc_user, rpc_password, method_name, args_num=0, params=(), **kwargs):
        super(DashRPCRequest, self).__init__(**kwargs)
        self.method = 'POST'
        self.url = self.base_url
        self.auth = HTTPBasicAuth(rpc_user, rpc_password)
        self.headers['Content-Type'] = 'text/plain'
        self.json = {
            'method': method_name,
            'jsonrpc': '1.0',
            'id': str(make_nonce()),
            'params': params[:args_num]
        }
