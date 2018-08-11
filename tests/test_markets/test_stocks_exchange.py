import requests_mock

from pycryptoclients.request import DEFAULT_USER_AGENT
from pycryptoclients.markets.stocks_exchange.api import StocksExchangeAPI
from pycryptoclients.markets.stocks_exchange.request import STOCKS_EXCHANGE_BASE_URL
from tests import CCAPITestCase
from tests.test_markets import *


class TestStocksExchangeAPI(CCAPITestCase):
    
    def setUp(self):
        super(TestStocksExchangeAPI, self).setUp()
        self.api = StocksExchangeAPI(api_secret=self.shared_secret, api_key=self.api_key)

    ######################################################
    # Test public API methods
    ######################################################

    @requests_mock.Mocker()
    def test_ticker(self, m):
        method_name = 'ticker'
        url = STOCKS_EXCHANGE_BASE_URL.format(method=method_name)
        m.register_uri('GET', url, text=TICKER_RESPONSE)
        data = self.api.call(method_name).data

        self.assertPublicMethod(method_name, m, url, DEFAULT_USER_AGENT)

        self.assertTrue(data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    @requests_mock.Mocker()
    def test_prices(self, m):
        method_name = 'prices'
        url = STOCKS_EXCHANGE_BASE_URL.format(method=method_name)
        m.register_uri('GET', url, text=PRICES_RESPONSE)
        data = self.api.call(method_name).data

        self.assertPublicMethod(method_name, m, url, DEFAULT_USER_AGENT)

        self.assertTrue(data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 3)

    @requests_mock.Mocker()
    def test_markets(self, m):
        method_name = 'markets'
        url = STOCKS_EXCHANGE_BASE_URL.format(method=method_name)
        m.register_uri('GET', url, text=MARKETS_RESPONSE)

        data = self.api.call(method_name).data
        self.assertPublicMethod(method_name, m, url, DEFAULT_USER_AGENT)
        self.assertTrue(data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    @requests_mock.Mocker()
    def test_currencies(self, m):
        method_name = 'currencies'
        url = STOCKS_EXCHANGE_BASE_URL.format(method=method_name)
        m.register_uri('GET', url, text=CURRENCIES_RESPONSE)

        data = self.api.call(method_name).data
        self.assertPublicMethod(method_name, m, url, DEFAULT_USER_AGENT)
        self.assertTrue(data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    @requests_mock.Mocker()
    def test_market_summary(self, m):
        method_name = 'market_summary'
        _method_url = '{}/BTC/USD'.format(method_name)
        url = STOCKS_EXCHANGE_BASE_URL.format(method=_method_url)

        m.register_uri('GET', url,
                       text=MARKET_SUMMARY_RESPONSE)

        data = self.api.call(method_name, currency1='BTC', currency2='USD').data
        self.assertPublicMethod(method_name, m, url, DEFAULT_USER_AGENT)
        self.assertTrue(data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

        with self.assertRaises(TypeError):
            self.api.call(method_name)  # currency1 and currency2 are required arguments for request

    @requests_mock.Mocker()
    def test_trade_history(self, m):
        method_name = 'trade_history'
        _currency1 = 'BTC'
        _currency2 = 'NXT'
        _method_url = '{}?pair={}_{}'.format('trades', _currency1, _currency2)
        url = STOCKS_EXCHANGE_BASE_URL.format(method=_method_url)

        m.register_uri('GET', url, text=TRADE_HISTORY_RESPONSE)

        data = self.api.call(method_name, currency1='BTC', currency2='NXT').data
        self.assertPublicMethod(method_name, m, url, DEFAULT_USER_AGENT)
        self.assertTrue(data)
        self.assertEqual(data['success'], 1)

        result = data['result']
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)

        with self.assertRaises(TypeError):
            self.api.call(method_name)  # currency1 and currency2 are required arguments for request

    @requests_mock.Mocker()
    def test_orderbook(self, m):
        method_name = 'orderbook'
        _currency1 = 'BTC'
        _currency2 = 'NXT'
        _method_url = '{}?pair={}_{}'.format(method_name, _currency1, _currency2)
        url = STOCKS_EXCHANGE_BASE_URL.format(method=_method_url)

        m.register_uri('GET', url, text=ORDERBOOK_RESPONSE)

        data = self.api.call(method_name, currency1='BTC', currency2='NXT').data
        self.assertPublicMethod(method_name, m, url, DEFAULT_USER_AGENT)
        self.assertTrue(data)
        self.assertEqual(data['success'], 1)

        result = data['result']
        self.assertIsInstance(result, dict)
        self.assertIn('buy', result)
        self.assertIn('sell', result)

        with self.assertRaises(TypeError):
            self.api.call(method_name)  # currency1 and currency2 are required arguments for request

    @requests_mock.Mocker()
    def test_public_grafic(self, m):
        method_name = 'grafic'
        _currency1 = 'BTC'
        _currency2 = 'NXT'
        _method_url = '{}?pair={}_{}&interval=1D&order=DESC&count=50'.format('grafic_public', _currency1,
                                                                             _currency2)
        url = STOCKS_EXCHANGE_BASE_URL.format(method=_method_url)
        m.register_uri('GET', url, text=PUBLIC_GRAFIC_RESPONSE)

        data = self.api.call(method_name, currency1='BTC', currency2='NXT').data
        self.assertPublicMethod(method_name, m, url, DEFAULT_USER_AGENT)
        self.assertTrue(data)
        self.assertEqual(data['success'], 1)

        result = data['data']
        self.assertIsInstance(result, dict)

        with self.assertRaises(TypeError):
            self.api.call(method_name)  # currency1 and currency2 are required arguments for request

    ######################################################
    # Test private API methods
    ######################################################

    def assertPrivateMethod(self, method_name, response_data, m, **request_params):
        m.register_uri('POST', STOCKS_EXCHANGE_BASE_URL.format(method=''), text=response_data)

        result = self.api.call(method_name, **request_params).data
        self.assertTrue(m.called)
        self.assertEqual(m.call_count, 1)
        self.assertAuth(m)
        self.assertTrue(result)
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('success'), 1)
        self.assertIn('data', result)

        req = m.request_history[0]
        req_headers = req.headers
        self.assertEqual(req_headers['User-Agent'], DEFAULT_USER_AGENT)
        self.assertEqual(req_headers['Content-Type'], 'application/json')
        return req

    @requests_mock.Mocker()
    def test_get_account_info(self, m):
        self.assertPrivateMethod('get_account_info', response_data=GET_ACCOUNT_INFO_RESPONSE, m=m)

    @requests_mock.Mocker()
    def test_get_active_orders(self, m):
        method_name = 'get_active_orders'
        self.assertPrivateMethod(method_name, response_data=GET_ACTIVE_ORDERS_RESPONSE, m=m)

        with self.assertRaises(ValueError):
            self.api.call(method_name, count=125)

    @requests_mock.Mocker()
    def test_trade(self, m):
        method_name = 'trade'
        self.assertPrivateMethod(method_name, response_data=TRADE_RESPONSE, m=m, _type='BUY', currency1='BTC',
                                 currency2='NXT', amount=2345, rate=1)

        with self.assertRaises(ValueError):
            self.api.call(method_name, _type='DUMP', currency1='BTC', currency2='NXT', amount=2345, rate=1)

        with self.assertRaises(ValueError):
            self.api.call(method_name, _type='BUY', currency1='BTC', currency2='NXT', amount=-235, rate=1)

        with self.assertRaises(ValueError):
            self.api.call(method_name, _type='BUY', currency1='BTC', currency2='NXT', amount=2345, rate=-1)

    @requests_mock.Mocker()
    def test_cancel_order(self, m):
        self.assertPrivateMethod('cancel_order', response_data=CANCEL_ORDER_RESPONSE, m=m, order_id=45)

    @requests_mock.Mocker()
    def test_private_trade_history(self, m):
        self.assertPrivateMethod('private_trade_history', response_data=PRIVATE_TRADE_HISTORY_RESPONSE, m=m)

    @requests_mock.Mocker()
    def test_transactions_history(self, m):
        method_name = 'transactions_history'
        self.assertPrivateMethod(method_name, response_data=TRANSACTIONS_HISTORY_RESPONSE, m=m)

        with self.assertRaises(ValueError):
            self.api.call(method_name, count=125)

    @requests_mock.Mocker()
    def test_private_grafic(self, m):
        method_name = 'private_grafic'
        self.assertPrivateMethod(method_name, response_data=PRIVATE_GRAFIC_RESPONSE, m=m)

        with self.assertRaises(ValueError):
            self.api.call(method_name, count=125)

    @requests_mock.Mocker()
    def test_deposit(self, m):
        self.assertPrivateMethod('deposit', response_data=DEPOSIT_RESPONSE, m=m, currency='BTC')

    @requests_mock.Mocker()
    def test_withdraw(self, m):
        self.assertPrivateMethod('withdraw', response_data=WITHDRAW_RESPONSE, m=m, currency='BTC',
                                 address='XXXXXXXX',
                                 amount=457.0)

    @requests_mock.Mocker()
    def test_generate_wallets(self, m):
        self.assertPrivateMethod('generate_wallets', response_data=GENERATE_WALLETS_RESPONSE, m=m, currency='BTC')

    @requests_mock.Mocker()
    def test_ticket(self, m):
        self.assertPrivateMethod('ticket', response_data=TICKET_RESPONSE, m=m, category=1,
                                 message='Can’t get deposit to my ETH wallet', subject='Can’t get deposit')

    @requests_mock.Mocker()
    def test_get_tickets(self, m):
        self.assertPrivateMethod('get_tickets', response_data=GET_TICKETS_RESPONSE, m=m, ticket_id=1,
                                 category=2, status=1)

    @requests_mock.Mocker()
    def test_reply_ticket(self, m):
        self.assertPrivateMethod('reply_ticket', response_data=REPLY_TICKET_RESPONSE, m=m, ticket_id=1,
                                 message='Some message')
