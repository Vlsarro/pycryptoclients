from pycryptoclients.api import CCRPC, APIMethod
from pycryptoclients.response import CCAPIResponseParser
from pycryptoclients.wallets.dash.request import GetInfoRequest


DEFAULT_RPC_METHODS = (
    APIMethod('getinfo', GetInfoRequest, CCAPIResponseParser),
)


class DashWalletRPCClient(CCRPC):

    def _init_default_api_methods(self):
        self.api_methods = {method.name: method for method in DEFAULT_RPC_METHODS}
