from base import Base

from kfp import Kfp

def factoryFunc(backend_name: str) -> Base:
    match backend_name:
        case 'kfp':
            return Kfp()
        case _:
            return Base()

