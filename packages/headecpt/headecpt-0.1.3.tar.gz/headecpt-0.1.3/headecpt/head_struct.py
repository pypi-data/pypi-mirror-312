import _io
import dataclasses
from enum import ReprEnum
from typing import Union, Optional
import hashlib

from headecpt.basic_struct import VersionType, IntType, ShortType, MD5Type, MetaDataLazyParser, LazyParser
from headecpt.encrypt_funcs import EncryptType
from headecpt.encrypt_funcs import encrypt_func_map, decrypt_func_map

MD5_MAX_SIZE = MD5Type.__byte_size__


def md5(data: bytes) -> bytes:
    return hashlib.md5(data).digest()[:MD5_MAX_SIZE]


class _Stream(object):
    def to_bytes(self) -> bytes:
        pass


class HeadInfo(_Stream):

    __magic__code__ = IntType.from_bytes(b'\x54\x63\x0e\x1a')

    magic_code: ShortType
    version: VersionType        # 编码版本
    encrypt_type: EncryptType   # 加密方式
    total_size: IntType         # 总文件大小
    pre_encrypt_size: IntType   # 加密前数据大小
    after_encrypt_size: IntType # 加密后数据大小
    extra_size: IntType         # 额外数据大小
    encrypt_md5: MD5Type        # 验证解码后数据正确与否的md5

    _struct = {
        'magic_code': IntType,
        'version': VersionType,        # 编码版本
        'encrypt_type': EncryptType,   # 加密方式
        'total_size': IntType,         # 总文件大小
        'pre_encrypt_size': IntType,   # 加密前数据大小
        'after_encrypt_size': IntType, # 加密后数据大小
        'extra_size': IntType,         # 额外数据大小
        'encrypt_md5': MD5Type,        # 验证解码后数据正确与否的md5
    }

    @classmethod
    def __len__(cls):
        return sum([item.__len__() for item in cls._struct.values()])

    @classmethod
    def from_bytes(cls, data: bytes):
        res = {}
        for key, type_class in cls._struct.items():
            if isinstance(type_class, LazyParser):
                type_class = type_class.update(res)
            res[key], data = type_class.parse(data)
        if len(data) > 0:
            raise ValueError(f'data is bigger than self, remains {len(data)}')
        return cls(**res)

    def __init__(self, *args, **kwargs):
        for (key_name, type_class), value in zip(self._struct.items(), args):
            type_class = self._struct[key_name]
            if isinstance(type_class, LazyParser):
                type_class = type_class.update(self)
            setattr(self, key_name, type_class(value))
        for key_name, value in kwargs.items():
            if key_name not in self._struct:
                raise KeyError(f'{key_name} cannot defined.')
            if getattr(self, key_name, None) is not None:
                raise ValueError(f'{key_name} have been defined in args: {getattr(self, key_name)}, '
                                 f'but you redefined it in kwargs as {value}')
            type_class = self._struct[key_name]
            if isinstance(type_class, LazyParser):
                type_class = type_class.update(self)
            setattr(self, key_name, type_class(value))
        for key_name in self._struct.keys():
            if getattr(self, key_name) is None:
                raise KeyError(f'did not defined the value of `{key_name}`')
        if self.magic_code != self.__magic__code__:
            raise ValueError('the magic number is not correct.')

    @property
    def tail_data_size(self):
        return (self.after_encrypt_size + self.extra_size) - self.head_data_size

    @property
    def head_data_size(self):
        return max(self.pre_encrypt_size - len(self), 0)

    def to_bytes(self):
        res = b''
        for key in self._struct:
            res += getattr(self, key).to_bytes()
        return res


@dataclasses.dataclass
class DynamicData(_Stream):
    extra_data: bytes
    after_encrypt_data: bytes

    def __len__(self):
        return len(self.extra_data) + len(self.after_encrypt_data)

    def to_bytes(self) -> bytes:
        return self.extra_data + self.after_encrypt_data
