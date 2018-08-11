import time
import random


__all__ = ('Dotdict', 'make_nonce', 'ENCODING', 'set_not_none_dict_kwargs')


ENCODING = 'utf-8'


class Dotdict(dict):
    def __getattr__(self, attr):
        return self.get(attr, None)


def make_nonce(makeweight: int=1000000) -> int:
    if not isinstance(makeweight, int) or makeweight < 0:
        raise ValueError(makeweight)
    return int(time.time()) * makeweight + random.randint(0, makeweight)


def set_not_none_dict_kwargs(dictionary: dict, **kwargs):
    if dictionary and isinstance(dictionary, dict):
        for k, v in kwargs.items():
            if v is not None:
                dictionary[k] = v
