import requests
from pycryptoclients.exc import CCAPIDataException
from pycryptoclients.response import CCAPIResponseParser


class DashRPCResponseParser(CCAPIResponseParser):

    @classmethod
    def parse(cls, response: requests.Response):
        cc_resp = super(DashRPCResponseParser, cls).parse(response)
        result = cc_resp.data.get('result')
        cls.check_for_errors(result)
        cc_resp.data = result
        return cc_resp

    @classmethod
    def check_for_errors(cls, data):
        error = data.get('error')
        if error:
            raise CCAPIDataException(msg=error)

        result_errors = data.get('errors')
        if result_errors:
            raise CCAPIDataException(msg=result_errors)
