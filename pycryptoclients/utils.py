import time
import random


__all__ = ('Dotdict', 'make_nonce', 'ENCODING')


ENCODING = 'utf-8'


class Dotdict(dict):
    def __getattr__(self, attr):
        return self.get(attr, None)


def make_nonce(makeweight: int=1000000) -> int:
    if not isinstance(makeweight, int) or makeweight < 0:
        raise ValueError(makeweight)
    return int(time.time()) * makeweight + random.randint(0, makeweight)
