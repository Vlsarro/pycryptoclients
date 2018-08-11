# pycryptoclients
Library which contains python clients for cryptocurrency markets and crypto wallets. Currently available exchanges:

* https://www.stocks.exchange/

## Installation

Clone repository and run ```setup.py```.

## Usage

```python
from pycryptoclients.markets.stocks_exchange.api import StocksExchangeAPI

api = StocksExchangeAPI()
ticker_data = api.call('ticker')
```

For private methods you have to provide api key and api secret and then initialize api as :

```python
from pycryptoclients.markets.stocks_exchange.api import StocksExchangeAPI

api = StocksExchangeAPI(api_key='apikey', api_secret='apisecret')
account_info = api.call('get_account_info')
```
If you want add some new methods to API object or override previous ones then you have to create custom request which inherits from ```StocksExchangeRequest```, example:

```python
from pycryptoclients.markets.stocks_exchange.api import StocksExchangeAPI, APIMethod
from pycryptoclients.markets.stocks_exchange.request import StocksExchangeRequest
from pycryptoclients.markets.stocks_exchange.response import StocksExchangeResponseParser

class MyNewRequest(StocksExchangeRequest):
  api_method = 'my_request'
  
my_new_method = APIMethod(name='myrequest', request=MyNewRequest, parser=StocksExchangeResponseParser)
api_methods = {my_new_method.name: my_new_method}

api = StocksExchangeAPI(api_methods=api_methods)
my_request_data = api.call('myrequest')
```
