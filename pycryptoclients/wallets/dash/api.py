from pycryptoclients.api import CCRPC


DEFAULT_RPC_METHODS = ()


class DashWalletRPCClient(CCRPC):

    def _init_default_api_methods(self):
        self.api_methods = {method.name: method for method in DEFAULT_RPC_METHODS}
