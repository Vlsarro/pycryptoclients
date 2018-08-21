from pycryptoclients.api import CCRPC, APIMethod
from pycryptoclients.wallets.dash.request import DashRPCRequest
from pycryptoclients.wallets.dash.response import DashRPCResponseParser


class RPCMethod(APIMethod):

    def __init__(self, args_num, *args):
        super(RPCMethod, self).__init__(*args)
        self.args_num = args_num


DASH_RPC_METHOD_ARG_NUM_DICT = {
    'getinfo': 0,
    'getaddressbalance': 0,
    'getaddressdeltas': 0,
    'getaddressmempool': 0,
    'getaddresstxids': 0,
    'getaddressutxos': 0,
    'verifymessage': 3,
    'getreceivedbyaddress': 2,
    'signmessage': 2
    # TODO: add all methods in similiar fashion
}

DEFAULT_DASH_RPC_METHODS = [RPCMethod(args_num, method_name, DashRPCRequest, DashRPCResponseParser)
                            for method_name, args_num in DASH_RPC_METHOD_ARG_NUM_DICT.items()]


class DashWalletRPCClient(CCRPC):

    def _init_default_api_methods(self):
        self.api_methods = {method.name: method for method in DEFAULT_DASH_RPC_METHODS}
