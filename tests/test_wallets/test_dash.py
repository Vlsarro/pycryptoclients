import json
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
        method_name = 'getinfo'

        resp = self.client.call(method_name)

        self.assertTrue(m.called)
        self.assertEqual(m.call_count, 1)

        req = m.request_history[0]
        self.assertEqual(req.method, 'POST')
        self.assertEqual(req.url, TEST_URL)
        req_body = req.json()
        self.assertEqual(req_body['method'], method_name)
        self.assertEqual(req_body['params'], [])

        req_headers = req.headers
        self.assertEqual(req_headers['User-Agent'], DEFAULT_USER_AGENT)
        self.assertEqual(req_headers['Content-Type'], 'text/plain')

        self.assertIsInstance(resp, CCAPIResponse)

        data = resp.data
        self.assertIsInstance(data, dict)
        self.assertDictEqual(json.loads(DASH_GETINFO_RESPONSE)['result'], data)

    @requests_mock.Mocker()
    def test_signmessage(self, m):
        m.register_uri('POST', TEST_URL, text=DASH_GETINFO_RESPONSE)
        method_name = 'signmessage'
        methods = self.client.get_available_methods()
        resp = self.client.call(method_name, 234, 455, 4565)

        self.assertTrue(m.called)
        self.assertEqual(m.call_count, 1)

        req = m.request_history[0]
        self.assertEqual(req.method, 'POST')
        self.assertEqual(req.url, TEST_URL)
        req_body = req.json()
        self.assertEqual(req_body['method'], method_name)
        self.assertEqual(req_body['params'], [234, 455])

        req_headers = req.headers
        self.assertEqual(req_headers['User-Agent'], DEFAULT_USER_AGENT)
        self.assertEqual(req_headers['Content-Type'], 'text/plain')

        self.assertIsInstance(resp, CCAPIResponse)

        data = resp.data
        self.assertIsInstance(data, dict)
        self.assertDictEqual(json.loads(DASH_GETINFO_RESPONSE)['result'], data)

if __name__ == '__main__':
    unittest.main()
