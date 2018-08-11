from requests import Request


__all__ = ('CCAPIRequest', 'BaseCCRequest', 'DEFAULT_USER_AGENT')


DEFAULT_USER_AGENT = 'pycryptoclients'


class BaseCCRequest(Request):
    api_method = None
    default_base_url = ''

    def __init__(self, base_url: str=None, **kwargs):
        super(BaseCCRequest, self).__init__()
        self.base_url = base_url if base_url else self.default_base_url
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': DEFAULT_USER_AGENT
        }
        self.method = 'GET'


class CCAPIRequest(BaseCCRequest):

    is_private = False

    def __init__(self, **kwargs):
        super(CCAPIRequest, self).__init__(**kwargs)
        self.url = self.base_url.format(method=self.api_method)
