from unittest import TestCase

from pycryptoclients.utils import set_not_none_dict_kwargs, make_nonce


class TestUtils(TestCase):

    def test_make_nonce(self):
        nonce = make_nonce()
        self.assertIsInstance(nonce, int)

        with self.assertRaises(ValueError):
            make_nonce('1234')

        with self.assertRaises(ValueError):
            make_nonce(-245643)

    def test_set_not_none_dict_kwargs(self):
        _dict = {
            'a': 23,
            'b': 44
        }

        set_not_none_dict_kwargs(_dict, c=45, d=None, e=0, f='')

        self.assertEqual(_dict['c'], 45)
        self.assertNotIn('d', _dict)
        self.assertEqual(_dict['e'], 0)
        self.assertEqual(_dict['f'], '')
