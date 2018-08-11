from pycryptoclients.response import CCAPIResponseParser
from pycryptoclients.exc import CCAPIDataException


class StocksExchangeResponseParser(CCAPIResponseParser):

    @classmethod
    def check_for_errors(cls, data):
        if isinstance(data, dict) and not int(data.get('success')):
            raise CCAPIDataException(msg=data.get('error'))
