import requests
import time
import threading
import warnings
from typing import Type

from pycryptoclients.exc import CCAPINoMethodException
from pycryptoclients.request import BaseCCRequest
from pycryptoclients.response import CCAPIResponseParser, CCAPIResponse
from pycryptoclients.utils import ENCODING


__all__ = ('APIMethod', 'BaseCCAPI', 'CCAPI', 'CCRPC')


try:
    import cachecontrol
    cache_adapter = cachecontrol.CacheControlAdapter()
except ImportError:
    warnings.warn('Caching is not enabled. Install CacheControl for cache enabling', ImportWarning)
    cache_adapter = None


class APIMethod(object):

    def __init__(self, name: str, request: Type[BaseCCRequest], parser: Type[CCAPIResponseParser]):
        self.name = name
        self.request = request
        self.parser = parser


class BaseCCAPI(object):
    SAVING_TIME_KEY = 'saving_time'

    def __init__(self, ssl_enabled: bool=True, api_methods: dict=None):
        super(BaseCCAPI, self).__init__()
        self.ssl_enabled = ssl_enabled
        self._init_default_api_methods()
        if api_methods:
            self.update_api_methods(api_methods)

    def _init_default_api_methods(self):
        self.api_methods = {}

    def update_api_methods(self, api_methods: dict):
        self.api_methods.update(api_methods)

    def get_available_methods(self):
        return self.api_methods.keys()

    def _query(self, req: requests.Request) -> requests.Response:
        sess = requests.Session()

        if cache_adapter:
            sess.mount('https://', cache_adapter)
            sess.mount('http://', cache_adapter)

        prepared_request = req.prepare()
        response = sess.send(prepared_request, verify=self.ssl_enabled)
        response.raise_for_status()
        return response

    def _query_with_saving(self, parser: Type[CCAPIResponseParser],
                           req: BaseCCRequest, **kwargs) -> CCAPIResponse:
        """
        Method enables user to save parsed response for specified time and prevents additional requests in
        this time interval. This method is convenient for ban avoidance in case of too frequent requests to API.

        Reentrant lock ensures thread safety of method.
        """
        unix_timestamp_now = time.time()

        saved_data_attr_name = '{}_data'.format(req.api_method)
        record_time_attr_name = '{}_time'.format(req.api_method)

        saving_time = kwargs.get(self.SAVING_TIME_KEY, 60.0)  # one minute by default

        with threading.RLock():
            if saving_time:
                # get saved values from previous requests if period of saving is set
                data = getattr(self, saved_data_attr_name, None)
                prev_record_time = getattr(self, record_time_attr_name, None)

                if not (data and prev_record_time and (unix_timestamp_now - prev_record_time) < saving_time):
                    data = parser.parse(self._query(req))
                    setattr(self, saved_data_attr_name, data)  # store parsed response in memory
                    setattr(self, record_time_attr_name,
                            unix_timestamp_now)  # save the recording time for response
            else:
                data = parser.parse(self._query(req))

            return data

    def query(self, parser: Type[CCAPIResponseParser], req: Type[BaseCCRequest],
              **kwargs) -> CCAPIResponse:
        _req = req(**kwargs)

        if any(k in kwargs for k in (self.SAVING_TIME_KEY, 'with_saving')):
            response = self._query_with_saving(parser, _req, **kwargs)
        else:
            response = parser.parse(self._query(_req))

        return response


class CCAPI(BaseCCAPI):
    """
    Client for cryptocurrency markets/exchanges
    """

    def __init__(self, ssl_enabled: bool=True, api_key: str='', api_secret: str='', api_methods: dict=None):
        super(CCAPI, self).__init__(ssl_enabled, api_methods)
        self._api_key = bytes(api_key, encoding=ENCODING)
        self._api_secret = bytes(api_secret, encoding=ENCODING)

    def call(self, method: str, **kwargs) -> CCAPIResponse:
        _method = self.api_methods.get(method)

        if not _method:
            raise CCAPINoMethodException(method=method)

        if _method.request.is_private:
            kwargs.update({
                'api_key': self._api_key,
                'api_secret': self._api_secret
            })

        return self.query(_method.parser, _method.request, **kwargs)


class CCRPC(BaseCCAPI):
    """
    RPC client for cryptowallets.
    """

    def __init__(self, ssl_enabled: bool=True, rpc_user: str='', rpc_password: str='', api_methods: dict=None,
                 rpc_url: str=''):
        super(CCRPC, self).__init__(ssl_enabled, api_methods)
        self._rpc_user = rpc_user
        self._rpc_password = rpc_password
        self._rpc_url = rpc_url

    def call(self, method: str, **kwargs) -> CCAPIResponse:
        _method = self.api_methods.get(method)

        if not _method:
            raise CCAPINoMethodException(method=method)

        kwargs.update({
            'rpc_user': self._rpc_user,
            'rpc_password': self._rpc_password,
            'base_url': self._rpc_url
        })

        return self.query(_method.parser, _method.request, **kwargs)
