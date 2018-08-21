import requests
import warnings

from pycryptoclients.exc import CCAPIResponseParsingException


class CCAPIResponse(object):

    def __init__(self, data, exc=None):
        self.data = data
        self.exc = exc


class CCAPIResponseParser(object):

    @classmethod
    def parse(cls, response: requests.Response) -> CCAPIResponse:
        try:
            data = response.json()
        except (ValueError, TypeError) as e:
            raise CCAPIResponseParsingException(exc=e, response=response)
        else:
            cls.check_for_errors(data)
            return CCAPIResponse(data)

    @classmethod
    def check_for_errors(cls, data):
        warnings.warn('{} has no error checking'.format(cls.__name__), stacklevel=2)
