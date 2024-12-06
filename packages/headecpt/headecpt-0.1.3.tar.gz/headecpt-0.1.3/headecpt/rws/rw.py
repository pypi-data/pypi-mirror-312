import _io
import os
from enum import ReprEnum
from typing import Union, Optional, Dict, Literal
import hashlib
import pickle as pk

from headecpt.basic_struct import VersionType, IntType, ShortType, MD5Type, MetaDataLazyParser, LazyParser
from headecpt.head_struct import HeadInfo, DynamicData
from headecpt.encrypt_funcs import EncryptType
from headecpt.encrypt_funcs import encrypt_func_map, decrypt_func_map, encrypt_str_map

MD5_MAX_SIZE = MD5Type.__byte_size__


def md5(data: bytes) -> bytes:
    return hashlib.md5(data).digest()[:MD5_MAX_SIZE]


class EncryptWriter(object):

    __version__ = VersionType.V1

    def __init__(self, path):
        self.path = path

        self.file_size: Optional[int] = None
        self.encrypt_type: Optional[EncryptType] = None
        self._file: Optional[_io.BufferedRandom] = None
        self.pre_encrypt_data: Optional[bytes] = None
        self.after_encrypt_data: Optional[bytes] = None
        self.extra_info: Dict = {}

        self.new_name = None

    @property
    def file(self) -> _io.BufferedRandom:
        if self._file is None or self._file.closed:
            self._file = open(self.path, 'r+b')
        return self._file

    def create_encrypt_info(self, head_size: Union[int, Literal['all']] = 1024,
                            encrypt_type: Union[EncryptType, str, None] = None, key='', extra_info=None):

        if isinstance(encrypt_type, str):
            encrypt_type = encrypt_str_map[encrypt_type]

        file_size = os.path.getsize(self.path)
        if isinstance(head_size, str) and head_size == 'all':
            head_size = file_size
        head_size = min(head_size, file_size)

        if head_size < HeadInfo.__len__():
            raise ValueError(f'Head size cannot less than {HeadInfo.__len__()}')

        self.file_size = file_size
        if encrypt_type is None:
            if key is None or len(key) <= 0:
                encrypt_type = EncryptType.REVERSE
            else:
                encrypt_type = EncryptType.RC4
        self.encrypt_type = encrypt_type

        self.file.seek(0, 0)
        self.pre_encrypt_data: bytes = self.file.read(head_size)
        self.after_encrypt_data = encrypt_func_map[encrypt_type](key, self.pre_encrypt_data)

        if extra_info is None:
            extra_info = {}
        self.extra_info = extra_info
        return self

    @property
    def extra_info_encode(self):
        if self.extra_info is None or len(self.extra_info) == 0:
            return b''
        else:
            return pk.dumps(self.extra_info)

    @property
    def head_info(self):
        return HeadInfo(HeadInfo.__magic__code__, VersionType.V1, self.encrypt_type,
                                  self.file_size,
                                  len(self.pre_encrypt_data), len(self.after_encrypt_data),
                                  len(self.extra_info_encode),
                                  md5(self.pre_encrypt_data))

    @property
    def dynamic_data(self):
        return DynamicData(self.extra_info_encode, self.after_encrypt_data)


    def encrypt(self):
        if self.head_info is None:
            raise ValueError('call `create_encrypt_info` first')
        self.file.seek(0, 0)
        self.file.write(self.head_info.to_bytes())

        dynamic_bytes = self.dynamic_data.to_bytes()
        self.file.write(dynamic_bytes[:self.head_info.head_data_size])

        assert self.head_info.tail_data_size == len(dynamic_bytes[self.head_info.head_data_size:])
        self.file.seek(0, 2)
        self.file.write(dynamic_bytes[self.head_info.head_data_size:])

        self.file.close()
        return self

    def encrypt_with_name(self, new_name=None):
        dir_path, filename = os.path.split(self.path)
        if new_name is None:
            new_name = hashlib.md5(self.path.encode('utf8')).hexdigest() + '.hep'
            self.new_name = new_name
        self.extra_info.update({'filename': filename})
        self.encrypt()
        self.rename(os.path.join(dir_path, new_name))
        return self

    def rename(self, new_name):
        if self._file is not None and not self._file.closed:
            self.file.close()
        os.rename(self.path, new_name)
        return self


class DecryptWriter(object):

    __version__ = VersionType.V1

    def __init__(self, path):
        self.path = path
        self._file: Optional[_io.BufferedRandom] = None

        self.head_info: Optional[HeadInfo] = None
        self.dynamic_data: Optional[DynamicData] = None
        self.new_path = None
        self.parse_decrypt_info()

    @property
    def file(self) -> _io.BufferedRandom:
        if self._file is None or self._file.closed:
            self._file = open(self.path, 'r+b')
        return self._file

    @property
    def extra_info(self) -> Dict:
        if len(self.dynamic_data.extra_data) == 0:
            return {}
        return pk.loads(self.dynamic_data.extra_data)

    def parse_decrypt_info(self):
        self.file.seek(0, 0)
        self.head_info = HeadInfo.from_bytes(self.file.read(HeadInfo.__len__()))
        data = self.file.read(self.head_info.head_data_size)

        self.file.seek(-1 * self.head_info.tail_data_size, 2)
        data += self.file.read(self.head_info.tail_data_size)
        self.dynamic_data = DynamicData(data[:self.head_info.extra_size], data[self.head_info.extra_size:])
        return self

    def decrypt(self, key=''):
        decrypt_data = decrypt_func_map[self.head_info.encrypt_type](key, self.dynamic_data.after_encrypt_data)
        assert len(decrypt_data) == self.head_info.pre_encrypt_size
        assert md5(decrypt_data) == self.head_info.encrypt_md5, f'(2) password is not correct.'
        self.file.seek(0, 0)
        self.file.write(decrypt_data)
        self.file.seek(self.head_info.total_size, 0)
        self.file.truncate()
        self.file.close()
        self.new_path = self.path
        if self.extra_info.get('filename'):
            self._decrypt_rename(self.extra_info.get('filename'))
        return self

    def _decrypt_rename(self, origin_filename):
        dir_path, _ = os.path.split(self.path)
        return self._rename(os.path.join(dir_path, origin_filename))

    def _rename(self, new_name):
        if self._file is not None and not self._file.closed:
            self.file.close()
        os.rename(self.path, new_name)
        self.new_path = new_name
        return self


if __name__ == '__main__':
    with open('../examples/test_data.txt', 'w') as f:
        for i in range(10):
            f.write(' '.join([f'{_}' for _ in range(10)]))
            f.write('\n')

    writer1 = EncryptWriter('../examples/test_data.txt')
    writer1.create_encrypt_info().encrypt()

    writer2 = DecryptWriter('../examples/test_data.txt')
    writer2.parse_decrypt_info().decrypt()


    with open('../examples/test_data.txt', 'w') as f:
        for i in range(1):
            f.write(' '.join([f'{_}' for _ in range(10)]))
            f.write('\n')

    writer1 = EncryptWriter('../examples/test_data.txt')
    writer1.create_encrypt_info(key='123').encrypt()

    writer2 = DecryptWriter('../examples/test_data.txt')
    writer2.parse_decrypt_info().decrypt(key='123')



    with open('../examples/test_data.txt', 'w') as f:
        for i in range(1):
            f.write(' '.join([f'{_}' for _ in range(10)]))
            f.write('\n')

    writer1 = EncryptWriter('../examples/test_data.txt')
    writer1.create_encrypt_info(key='123').encrypt_with_name()

    writer2 = DecryptWriter('../examples/63290f3921b62563810af8bc47c346d7.hep')
    writer2.parse_decrypt_info().decrypt(key='123')

