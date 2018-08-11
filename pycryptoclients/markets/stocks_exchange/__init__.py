from pycryptoclients.utils import Dotdict


__all__ = ('ORDER_STATUS',)


ORDER_STATUS = Dotdict(PENDING=1, PROCESSING=2, FINISHED=3, CANCELED=4)
