from pycryptoclients.auth import HmacAuth
from pycryptoclients.request import CCAPIRequest
from pycryptoclients.markets.stocks_exchange import ORDER_STATUS
from pycryptoclients.markets.stocks_exchange.utils import set_not_none_dict_kwargs


__all__ = ('TickerRequest', 'PricesRequest', 'CurrenciesRequest', 'MarketsRequest',
           'MarketSummaryRequest', 'TradeHistoryRequest', 'OrderbookRequest', 'GraficPublicRequest', 'DepositRequest',
           'GetAccountInfoRequest', 'GetActiveOrdersRequest', 'TradeRequest', 'CancelOrderRequest', 'WithdrawRequest',
           'PrivateTradeHistoryRequest', 'TransactionHistoryRequest', 'GraficPrivateRequest', 'GenerateWalletsRequest',
           'TicketRequest', 'GetTicketsRequest', 'ReplyTicketRequest')


class StocksExchangeRequest(CCAPIRequest):
    default_base_url = 'https://app.stocks.exchange/api2/{method}'


###################################################################
# Requests for public methods
###################################################################


class TickerRequest(StocksExchangeRequest):
    api_method = 'ticker'


class PricesRequest(StocksExchangeRequest):
    api_method = 'prices'


class CurrenciesRequest(StocksExchangeRequest):
    api_method = 'currencies'


class MarketsRequest(StocksExchangeRequest):
    api_method = 'markets'


class MarketSummaryRequest(StocksExchangeRequest):
    api_method = 'market_summary'

    def __init__(self, currency1: str, currency2: str, **kwargs):
        super(MarketSummaryRequest, self).__init__(**kwargs)
        self.url = self.base_url.format(method=self.api_method) + '/{}/{}'.format(currency1, currency2)


class TradeHistoryRequest(StocksExchangeRequest):
    api_method = 'trades'

    def __init__(self, currency1: str, currency2: str, **kwargs):
        super(TradeHistoryRequest, self).__init__(**kwargs)
        self.params.update(pair='{}_{}'.format(currency1, currency2))


class OrderbookRequest(TradeHistoryRequest):
    api_method = 'orderbook'


DEFAULT_ORDER = 'DESC'
DEFAULT_COUNT = 50
DEFAULT_INTERVAL = '1D'


class GraficPublicRequest(StocksExchangeRequest):
    api_method = 'grafic_public'

    def __init__(self, currency1: str, currency2: str, order: str = DEFAULT_ORDER, count: int = DEFAULT_COUNT,
                 interval: str = DEFAULT_INTERVAL, since: str = None, end: str = None, **kwargs):
        super(GraficPublicRequest, self).__init__(**kwargs)
        params = {
            'pair': '{}_{}'.format(currency1, currency2),
            'interval': interval,
            'order': order,
            'count': count
        }
        set_not_none_dict_kwargs(params, since=since, end=end)
        self.params.update(params)


###################################################################
# Requests for private methods
###################################################################


class StockExchangePrivateRequest(StocksExchangeRequest):
    is_private = True

    def __init__(self, api_key: str, api_secret: str, **kwargs):
        super(StockExchangePrivateRequest, self).__init__(**kwargs)
        self.auth = HmacAuth(api_key=api_key, api_secret=api_secret)
        self.url = self.base_url.format(method='')
        self.method = 'POST'
        self.json = {
            'method': self.api_method
        }


class GetAccountInfoRequest(StockExchangePrivateRequest):
    api_method = 'GetInfo'


DEFAULT_TYPE = 'ALL'
DEFAULT_OWNER = 'OWN'


class GetActiveOrdersRequest(StockExchangePrivateRequest):
    api_method = 'ActiveOrders'

    def __init__(self, _from: str = None, from_id: str = None, end_id: str = None, since: str = None, end: str = None,
                 pair: str = DEFAULT_TYPE, count: int = DEFAULT_COUNT, order: str = DEFAULT_ORDER,
                 _type: str = DEFAULT_TYPE,
                 owner: str = DEFAULT_OWNER, **kwargs):
        super(GetActiveOrdersRequest, self).__init__(**kwargs)

        if count and count > DEFAULT_COUNT:
            raise ValueError('count cannot be greater than {}. Currently: {} {}'.format(DEFAULT_COUNT, count,
                                                                                        type(count)))

        request_data = {
            'pair': pair,
            'count': count,
            'order': order,
            'type': _type,
            'owner': owner
        }

        optional_none_params = {
            'from': _from,
            'from_id': from_id,
            'end_id': end_id,
            'since': since,
            'end': end
        }
        set_not_none_dict_kwargs(request_data, **optional_none_params)

        self.json.update(request_data)


class TradeRequest(StockExchangePrivateRequest):
    api_method = 'Trade'

    def __init__(self, _type: str, currency1: str, currency2: str, amount: float, rate: float, **kwargs):
        super(TradeRequest, self).__init__(**kwargs)

        if amount and amount < 0:
            raise ValueError('amount must be positive float number. Currently: {} {}'.format(amount, type(amount)))

        if rate and rate < 0:
            raise ValueError('rate must be positive float number. Currently: {} {}'.format(rate, type(rate)))

        if _type and _type not in ('BUY', 'SELL'):
            raise ValueError('The parameter type can be one of "BUY" or "SELL". Currently: {} {}'.format(_type,
                                                                                                         type(_type)))

        self.json.update({
            'pair': '{}_{}'.format(currency1, currency2),
            'type': _type,
            'amount': amount,
            'rate': rate
        })


class CancelOrderRequest(StockExchangePrivateRequest):
    api_method = 'CancelOrder'

    def __init__(self, order_id: int, **kwargs):
        super(CancelOrderRequest, self).__init__(**kwargs)
        self.json.update(order_id=order_id)


class PrivateTradeHistoryRequest(StockExchangePrivateRequest):
    api_method = 'TradeHistory'

    def __init__(self, _from: int = None, from_id: str = None, end_id: str = None, since: str = None, end: str = None,
                 pair: str = 'ALL', count: int = DEFAULT_COUNT, order: str = DEFAULT_ORDER, owner: str = DEFAULT_OWNER,
                 status: int = 3, **kwargs):
        super(PrivateTradeHistoryRequest, self).__init__(**kwargs)
        self.json.update({
            'pair': pair,
            'from': _from,
            'count': count,
            'from_id': from_id,
            'end_id': end_id,
            'order': order,
            'since': since,
            'end': end,
            'status': status,
            'owner': owner
        })


class TransactionHistoryRequest(StockExchangePrivateRequest):
    api_method = 'TransHistory'

    def __init__(self, currency: str = DEFAULT_TYPE, _from: int = None, count: int = DEFAULT_COUNT, from_id: int = None,
                 end_id: int = None, order: str = DEFAULT_ORDER, since: str = None, end: str = None,
                 status: int = ORDER_STATUS.FINISHED, **kwargs):
        super(TransactionHistoryRequest, self).__init__(**kwargs)

        # FIXME: similar to StockExchangeGetActiveOrdersRequest

        if count and count > DEFAULT_COUNT:
            raise ValueError('count cannot be greater than {}. Currently: {} {}'.format(DEFAULT_COUNT, count,
                                                                                        type(count)))

        request_data = {
            'currency': currency,
            'count': count,
            'order': order,
            'status': status
        }
        optional_none_params = {
            'from': _from,
            'from_id': from_id,
            'end_id': end_id,
            'since': since,
            'end': end
        }
        set_not_none_dict_kwargs(request_data, **optional_none_params)
        self.json.update(request_data)


class GraficPrivateRequest(StockExchangePrivateRequest):
    api_method = 'Grafic'

    def __init__(self, pair: str = DEFAULT_TYPE, order: str = DEFAULT_ORDER, count: int = DEFAULT_COUNT,
                 interval: str = DEFAULT_INTERVAL, page: int = 1, since: str = None, end: str = None, **kwargs):
        super(GraficPrivateRequest, self).__init__(**kwargs)

        # FIXME: similiar to GraficPublicRequest

        if count and count > 100:
            raise ValueError('count cannot be greater than {}. Currently: {} {}'.format(100, count,
                                                                                        type(count)))

        request_data = {
            'pair': pair,
            'order': order,
            'count': count,
            'interval': interval,
            'page': page
        }
        set_not_none_dict_kwargs(request_data, since=since, end=end)

        self.json.update(request_data)


class DepositRequest(StockExchangePrivateRequest):
    api_method = 'Deposit'

    def __init__(self, currency: str, **kwargs):
        super(DepositRequest, self).__init__(**kwargs)
        self.json.update(currency=currency)


class WithdrawRequest(StockExchangePrivateRequest):
    api_method = 'Withdraw'

    def __init__(self, currency: str, address: str, amount: float, **kwargs):
        super(WithdrawRequest, self).__init__(**kwargs)
        self.json.update({
            'currency': currency,
            'address': address,
            'amount': amount
        })


class GenerateWalletsRequest(DepositRequest):
    api_method = 'GenerateWallets'


class TicketRequest(StockExchangePrivateRequest):
    api_method = 'Ticket'

    def __init__(self, category: int, subject: str, message: str, currency_name=None, **kwargs):
        super(TicketRequest, self).__init__(**kwargs)
        request_data = {
            'category': category,
            'subject': subject,
            'message': message
        }

        if currency_name:
            request_data['currency_name'] = currency_name

        self.json.update(request_data)


class GetTicketsRequest(StockExchangePrivateRequest):
    api_method = 'GetTickets'

    def __init__(self, ticket_id: int, category: int, status: int, **kwargs):
        super(GetTicketsRequest, self).__init__(**kwargs)
        self.json.update({
            'ticket_id': ticket_id,
            'category': category,
            'status': status
        })


class ReplyTicketRequest(StockExchangePrivateRequest):
    api_method = 'ReplyTicket'

    def __init__(self, ticket_id: int, message: str, **kwargs):
        super(ReplyTicketRequest, self).__init__(**kwargs)
        self.json.update({
            'ticket_id': ticket_id,
            'message': message
        })
