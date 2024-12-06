from enum import ReprEnum
from typing import Tuple, Any, Dict


class _Struct(object):

    @classmethod
    def from_bytes(cls, data: bytes):
        pass

    @classmethod
    def parse(cls, data: bytes) -> Tuple[Any, bytes]:
        y = cls.from_bytes(data[:cls.__len__()])
        return y, data[len(y):]  # noqa


class _IntType(int, _Struct):

    __byte_size__ = None

    def to_bytes(self):  # noqa
        return super().to_bytes(self.__byte_size__, "big", signed=False)

    @classmethod
    def from_bytes(cls, _bytes, byteorder = "big", *, signed = False):
        if len(_bytes) != cls.__byte_size__ or byteorder !="big" or signed != False:
            raise ValueError
        return super().from_bytes(_bytes, "big", signed=signed)

    @classmethod
    def __len__(cls):
        return cls.__byte_size__


class _Bytes(bytes, _Struct):

    __byte_size__ = None

    def __new__(cls, *args, **kwargs):
        arg_length = len(args[0])
        if arg_length != cls.__len__():
            raise ValueError(f'data length {arg_length} is not equal to {cls.__name__} length {cls.__len__()}')
        return super().__new__(cls, *args, **kwargs)

    def to_bytes(self) -> bytes:
        return self

    @classmethod
    def from_bytes(cls, _bytes):
        if len(_bytes) < cls.__len__():
            raise ValueError(f'data length {len(_bytes)} is less than {cls.__name__} length {cls.__len__()}')
        return cls(_bytes[:cls.__len__()])

    @classmethod
    def __len__(cls):
        return cls.__byte_size__


class MD5Type(_Bytes):
    __byte_size__ = 8


class IntType(_IntType):
    __byte_size__ = 4


class ShortType(_IntType):
    __byte_size__ = 2


class CharType(_IntType):
    __byte_size__ = 1


class ShortSizeEnum(ShortType, ReprEnum):
    pass


class VersionType(CharType):
    V1 = 0


class LazyParser(object):

    def update(self, data) -> type:
        pass


class MetaDataLazyParser(LazyParser):

    def __init__(self, size_param_name: str):
        self.size_param_name = size_param_name
        self.data = None

    def update(self, data) -> type:
        self.data = data
        return self.meta_data_class

    @property
    def size(self):
        if isinstance(self.data, Dict):
            return self.data[self.size_param_name]
        return getattr(self.data, self.size_param_name)

    @property
    def meta_data_class(self):

        class MetaData(_Bytes):
            __byte_size__ = self.size

        return MetaData
