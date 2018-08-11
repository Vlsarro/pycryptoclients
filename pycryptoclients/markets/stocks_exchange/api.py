from pycryptoclients.api import APIMethod, CCAPI
from pycryptoclients.markets.stocks_exchange.request import *
from pycryptoclients.markets.stocks_exchange.response import StocksExchangeResponseParser


DEFAULT_STOCKS_EXCHANGE_API_METHODS = (

    # Public methods

    APIMethod(name='ticker', request=TickerRequest, parser=StocksExchangeResponseParser),
    APIMethod(name='prices', request=PricesRequest, parser=StocksExchangeResponseParser),
    APIMethod(name='currencies', request=CurrenciesRequest, parser=StocksExchangeResponseParser),
    APIMethod(name='markets', request=MarketsRequest, parser=StocksExchangeResponseParser),
    APIMethod(name='market_summary', request=MarketSummaryRequest, parser=StocksExchangeResponseParser),
    APIMethod(name='trade_history', request=TradeHistoryRequest, parser=StocksExchangeResponseParser),
    APIMethod(name='orderbook', request=OrderbookRequest, parser=StocksExchangeResponseParser),
    APIMethod(name='grafic', request=GraficPublicRequest, parser=StocksExchangeResponseParser),

    # Private methods

    APIMethod(name='get_account_info', request=GetAccountInfoRequest, parser=StocksExchangeResponseParser),
    APIMethod(name='get_active_orders', request=GetActiveOrdersRequest, parser=StocksExchangeResponseParser),
    APIMethod(name='trade', request=TradeRequest, parser=StocksExchangeResponseParser),
    APIMethod(name='cancel_order', request=CancelOrderRequest, parser=StocksExchangeResponseParser),
    APIMethod(name='private_trade_history', request=PrivateTradeHistoryRequest, parser=StocksExchangeResponseParser),
    APIMethod(name='transactions_history', request=TransactionHistoryRequest, parser=StocksExchangeResponseParser),
    APIMethod(name='private_grafic', request=GraficPrivateRequest, parser=StocksExchangeResponseParser),
    APIMethod(name='deposit', request=DepositRequest, parser=StocksExchangeResponseParser),
    APIMethod(name='withdraw', request=WithdrawRequest, parser=StocksExchangeResponseParser),
    APIMethod(name='generate_wallets', request=GenerateWalletsRequest, parser=StocksExchangeResponseParser),
    APIMethod(name='ticket', request=TicketRequest, parser=StocksExchangeResponseParser),
    APIMethod(name='get_tickets', request=GetTicketsRequest, parser=StocksExchangeResponseParser),
    APIMethod(name='reply_ticket', request=ReplyTicketRequest, parser=StocksExchangeResponseParser),
)


class StocksExchangeAPI(CCAPI):

    def _init_default_api_methods(self):
        self.api_methods = {method.name: method for method in DEFAULT_STOCKS_EXCHANGE_API_METHODS}
