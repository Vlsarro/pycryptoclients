from requests import Request


__all__ = ('CCAPIRequest', 'DEFAULT_USER_AGENT')


DEFAULT_USER_AGENT = 'pycryptoclients'


class CCAPIRequest(Request):
    api_method = None
    is_private = False
    default_base_url = ''

    def __init__(self, base_url: str=None, **kwargs):
        super(CCAPIRequest, self).__init__()
        self.base_url = base_url if base_url else self.default_base_url
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': DEFAULT_USER_AGENT
        }
        self.url = self.base_url.format(method=self.api_method)
        self.method = 'GET'
