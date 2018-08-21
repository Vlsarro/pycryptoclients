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


ONE_MINUTE = 60.0


class BaseCCAPI(object):

    def __init__(self, ssl_enabled: bool=True, api_methods: dict=None):
        super(BaseCCAPI, self).__init__()
        self._lock = threading.RLock()
        self.saved_data = {}
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

    def _save_query(self, parser: Type[CCAPIResponseParser], req: BaseCCRequest, saving_id: str,
                    timestamp: float, has_data_by_id: bool=True) -> CCAPIResponse:
        with self._lock:
            response_data = parser.parse(self._query(req))
            response = {
                'data': response_data,
                'time': timestamp
            }

            if has_data_by_id:
                self.saved_data[saving_id][req.api_method] = response

            else:
                self.saved_data[saving_id] = {
                    req.api_method: response
                }

            return response_data

    def _query_with_saving(self, parser: Type[CCAPIResponseParser], req: BaseCCRequest, saving_id: str,
                           saving_time: float) -> CCAPIResponse:
        """
        Method enables user to save parsed response for specified time and prevents additional requests in
        this time interval. This method is convenient for ban avoidance in case of too frequent requests to API.

        Reentrant lock ensures thread safety of method.
        """

        # TODO: think about data storing backends (e.g. memcached, redis)

        with self._lock:
            unix_timestamp_now = time.time()

            if saving_time:
                # get saved values from previous requests if period of saving is set
                saved_data_by_id = self.saved_data.get(saving_id)

                if saved_data_by_id:
                    response = saved_data_by_id.get(req.api_method)

                    if response:
                        prev_record_time = response['time']
                        response_data = response['data']

                        if not (prev_record_time and (unix_timestamp_now - prev_record_time) < saving_time):
                            response_data = self._save_query(parser, req, saving_id, unix_timestamp_now)

                    else:
                        response_data = self._save_query(parser, req, saving_id, unix_timestamp_now)

                else:
                    response_data = self._save_query(parser, req, saving_id, unix_timestamp_now, has_data_by_id=False)

            else:
                response_data = parser.parse(self._query(req))

            return response_data

    def query(self, parser: Type[CCAPIResponseParser], req: Type[BaseCCRequest], saving_id: str=None,
              saving_time: float=None, **kwargs) -> CCAPIResponse:
        _req = req(**kwargs)

        if saving_id:
            response = self._query_with_saving(parser, _req, saving_id, saving_time)
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

    def call(self, method: str, saving_id: str=None, saving_time: float=ONE_MINUTE, **kwargs) -> CCAPIResponse:
        _method = self.api_methods.get(method)

        if not _method:
            raise CCAPINoMethodException(method=method)

        if _method.request.is_private:
            kwargs.update({
                'api_key': self._api_key,
                'api_secret': self._api_secret
            })

        return self.query(_method.parser, _method.request, saving_id=saving_id, saving_time=saving_time, **kwargs)


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

    def call(self, method: str, call_args: tuple=(), saving_id: str=None, saving_time: float=ONE_MINUTE,
             **kwargs) -> CCAPIResponse:
        _method = self.api_methods.get(method)

        if not _method:
            raise CCAPINoMethodException(method=method)

        if not call_args or not isinstance(call_args, (list, tuple)):
            call_args = ()

        kwargs.update({
            'rpc_user': self._rpc_user,
            'rpc_password': self._rpc_password,
            'base_url': self._rpc_url,
            'params': call_args,
            'args_num': _method.args_num,
            'method_name': method
        })

        return self.query(_method.parser, _method.request, saving_id=saving_id, saving_time=saving_time, **kwargs)
