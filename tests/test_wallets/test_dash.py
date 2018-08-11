import unittest
import requests_mock

from pycryptoclients.request import DEFAULT_USER_AGENT
from pycryptoclients.response import CCAPIResponse
from pycryptoclients.wallets.dash.api import DashWalletRPCClient
from tests.test_wallets import DASH_GETINFO_RESPONSE


TEST_URL = 'http://127.0.0.1:7423/'


class TestDashWalletRPCClient(unittest.TestCase):

    def setUp(self):
        super(TestDashWalletRPCClient, self).setUp()
        self.client = DashWalletRPCClient(rpc_user='test_user', rpc_password='test_1', rpc_url=TEST_URL)

    @requests_mock.Mocker()
    def test_getinfo(self, m):
        m.register_uri('POST', TEST_URL, text=DASH_GETINFO_RESPONSE)

        resp = self.client.call('getinfo')

        self.assertTrue(m.called)
        self.assertEqual(m.call_count, 1)

        req = m.request_history[0]
        self.assertEqual(req.method, 'POST')
        self.assertEqual(req.url, TEST_URL)

        req_headers = req.headers
        self.assertEqual(req_headers['User-Agent'], DEFAULT_USER_AGENT)
        self.assertEqual(req_headers['Content-Type'], 'text/plain')

        self.assertIsInstance(resp, CCAPIResponse)

        data = resp.data
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data['result'], dict)
        self.assertIsNone(data['error'])


if __name__ == '__main__':
    unittest.main()
