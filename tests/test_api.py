import json
import requests
import requests_mock
import unittest
from unittest.mock import patch

from pycryptoclients.api import CCAPI, APIMethod
from pycryptoclients.exc import CCAPINoMethodException
from pycryptoclients.request import CCAPIRequest, DEFAULT_USER_AGENT
from pycryptoclients.response import CCAPIResponseParser
from tests import CCAPITestCase


base_url = 'http://example.com/{method}'
method_name = 'get_info'
test_response = json.dumps([
    {
        'min_order_amount': '0.00000010',
        'ask': '0.000033',
        'bid': '0.00002905',
        'last': '0.00002905',
        'lastDayAgo': '0.00003094',
        'vol': '2665.35219464',
        'spread': '0',
        'buy_fee_percent': '0',
        'sell_fee_percent': '0',
        'market_name': 'MUN_BTC',
        'updated_time': 1520779505,
        'server_time': 1520779505
    }
])


class TestRequest(CCAPIRequest):
    api_method = method_name

    default_base_url = base_url


class TestAPI(CCAPI):

    def _init_default_api_methods(self):
        self.api_methods = {'get_info': APIMethod('get_info', TestRequest, CCAPIResponseParser)}


class TestCCAPI(CCAPITestCase):

    def setUp(self):
        super(TestCCAPI, self).setUp()
        self.api = TestAPI()

    @requests_mock.Mocker()
    def test_query(self, m):
        url = base_url.format(method=method_name)
        m.register_uri('GET', url, text=test_response)

        _req = TestRequest()
        response = self.api._query(_req)

        self.assertPublicMethod(method_name, m, url, user_agent=DEFAULT_USER_AGENT)
        self.assertIsInstance(response, requests.Response)

    @requests_mock.Mocker()
    def test_public_query(self, m):
        # test with predefined ticker request
        url = base_url.format(method=method_name)
        m.register_uri('GET', url, text=test_response)
        data = self.api.query(CCAPIResponseParser, TestRequest)

        self.assertPublicMethod(method_name, m, url=url, user_agent=DEFAULT_USER_AGENT)
        self.assertTrue(data)

        # test queries with saving
        with patch('time.time') as time_mock:
            time_mock.return_value = 130.0

            saving_id = 'test'
            saving_time = 60.0

            data = self.api.query(CCAPIResponseParser, TestRequest, saving_id, saving_time)
            self.assertEqual(m.call_count, 2)
            self.assertTrue(data)

            time_mock.return_value = 140.0
            data = self.api.query(CCAPIResponseParser, TestRequest, saving_id, saving_time)
            self.assertEqual(m.call_count, 2)  # no call because time has not passed yet
            self.assertTrue(data)

            # change threshold to 5 seconds
            data = self.api.query(CCAPIResponseParser, TestRequest, saving_id, 5.0)
            self.assertEqual(m.call_count, 3)
            self.assertTrue(data)

    def test_get_available_methods(self):
        available_methods = self.api.get_available_methods()
        self.assertIn('get_info', available_methods)

    def test_raise_on_absent_method(self):
        with self.assertRaises(CCAPINoMethodException) as cm:
            self.api.call('karabas')

        self.assertEqual(cm.exception.msg, 'API does not provide <karabas> method')

    def test_update_methods(self):
        new_method_name = 'newmethod'
        new_method = APIMethod(name=new_method_name, request=TestRequest, parser=CCAPIResponseParser)
        new_methods = {new_method.name: new_method}

        new_api = TestAPI(api_methods=new_methods)
        self.assertIn(new_method_name, new_api.get_available_methods())

        self.assertNotIn(new_method_name, self.api.get_available_methods())
        self.api.update_api_methods(api_methods=new_methods)
        self.assertIn(new_method_name, self.api.get_available_methods())

    @patch('time.time')
    @requests_mock.Mocker()
    def test_query_with_saving(self, time_mock, m):
        # test with predefined ticker request
        url = base_url.format(method=method_name)
        m.register_uri('GET', url, text=test_response)
        time_mock.return_value = 130.0

        saving_id = 'test'
        saving_time = 60.0

        self.assertDictEqual(self.api._saved_data, {})

        data = self.api._query_with_saving(CCAPIResponseParser, TestRequest(), saving_id, saving_time).data
        self.assertTrue(m.called)
        self.assertEqual(m.call_count, 1)
        self.assertTrue(data)

        self.assertIn(saving_id, self.api._saved_data)
        self.assertIn(method_name, self.api._saved_data[saving_id])

        time_mock.return_value = 140.0
        data = self.api._query_with_saving(CCAPIResponseParser, TestRequest(), saving_id, saving_time).data
        self.assertEqual(m.call_count, 1)  # there was no call to API, use saved response
        self.assertTrue(data)

        time_mock.return_value = 189.9
        data = self.api._query_with_saving(CCAPIResponseParser, TestRequest(), saving_id, saving_time).data
        self.assertEqual(m.call_count, 1)  # there was no call to API, use saved response
        self.assertTrue(data)

        time_mock.return_value = 191.0
        data = self.api._query_with_saving(CCAPIResponseParser, TestRequest(), saving_id, saving_time).data
        self.assertEqual(m.call_count, 2)
        self.assertTrue(data)

        time_mock.return_value = 200
        saving_id_2 = 'test_2'
        data = self.api._query_with_saving(CCAPIResponseParser, TestRequest(), saving_id_2, saving_time).data
        self.assertEqual(m.call_count, 3)
        self.assertTrue(data)

        self.assertIn(saving_id_2, self.api._saved_data)
        self.assertIn(method_name, self.api._saved_data[saving_id_2])


if __name__ == '__main__':
    unittest.main()
