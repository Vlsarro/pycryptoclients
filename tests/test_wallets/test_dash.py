import unittest

from pycryptoclients.wallets.dash.api import DashWalletRPCClient


class TestDashWalletRPCClient(unittest.TestCase):

    def setUp(self):
        super(TestDashWalletRPCClient, self).setUp()
        self.wallet_client = DashWalletRPCClient()
