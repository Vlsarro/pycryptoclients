import hashlib
import hmac
import unittest

from pycryptoclients.utils import ENCODING


class CCAPITestCase(unittest.TestCase):

    def setUp(self):
        super(CCAPITestCase, self).setUp()
        self.shared_secret = 'KW9Wixy1zj9uNyzOjFbPu7YmU4iVJ1n3lEzqVAe5byx93IwugVQdlhoN03MzZW75'
        self.api_key = 'ak9uh9ezAK3w7FivoRdEnIFjBg7Ywjz4sImOpIzE'

    def assertAuth(self, m):
        req = m.request_history[0]
        req_signdata = bytearray(req.text, encoding=ENCODING)
        req_sign = bytes(req.headers['Sign'], encoding=ENCODING)
        sign = bytes(hmac.new(bytes(self.shared_secret, encoding=ENCODING), req_signdata, hashlib.sha512).hexdigest(),
                     encoding=ENCODING)
        self.assertTrue(hmac.compare_digest(req_sign, sign), msg='Calculated sign: {}\n'
                                                                 'Sign in request: {}'.format(sign, req_sign))

    def assertPublicMethod(self, method_name, m, url, user_agent, content_type='application/json', method='GET'):
        self.assertTrue(m.called)
        self.assertEqual(m.call_count, 1)

        req = m.request_history[0]
        self.assertEqual(req.method, method)
        self.assertEqual(req.url, url.format(method_name))

        req_headers = req.headers
        self.assertEqual(req_headers['User-Agent'], user_agent)
        self.assertEqual(req_headers['Content-Type'], content_type)

        return req
