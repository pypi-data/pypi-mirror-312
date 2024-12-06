import os
import logging
import click

from headecpt import __version__
from headecpt.rws.rw import EncryptWriter, DecryptWriter
from headecpt.encrypt_funcs import encrypt_str_map


logging.basicConfig(level=logging.INFO)


class IntOrStrType(click.ParamType):
    name = 'int_or_str'

    def convert(self, value, param, ctx):
        try:
            return int(value)
        except ValueError:
            return value


@click.group()
@click.option('-v', '--version', is_flag=True)
def main(version):
    if version:
        print(__version__)


@main.command(help="Encrypt the files")
@click.argument('path', type=click.Path(exists=True), nargs=-1)
@click.option('-t', '--type', default=None, type=click.Choice(list(encrypt_str_map.keys())),
              help="加密方式：no为无密钥加密，rc4为有密钥加密")
@click.option('-h', '--head_size', default=1024, type=IntOrStrType(), help="待加密文件头大小")
@click.option('-p', '--password', hide_input=True, confirmation_prompt=True, default='',
              help="加密密钥，若不指定则默认no加密方法，指定则默认为rc4方法")
@click.option('--remain_name', is_flag=True,
              help="是否对文件名进行加密，默认加密，若不加密则指定--without-name")
def en(path, head_size, type, password, remain_name):
    if len(path) <= 0:
        logging.error('You must input a file path.')
    for p in path:
        try:
            if remain_name:
                EncryptWriter(p).create_encrypt_info(head_size, type, password).encrypt()
                logging.info(f'Encrypt: {p}')
            else:
                res = EncryptWriter(p).create_encrypt_info(head_size, type, password).encrypt_with_name()
                logging.info(f'Encrypt: {p} --> {res.new_name}')
        except Exception as e:
            logging.error(f'{e}')


@main.command(help="Decrypt the files")
@click.argument('path', type=click.Path(exists=True), nargs=-1)
@click.option('-p', '--password', hide_input=True, confirmation_prompt=True, default='',
              help="解密密钥")
def de(path, password = ''):
    if len(path) <= 0:
        logging.error('You must input a file path.')
    for p in path:
        try:
            res = DecryptWriter(p).parse_decrypt_info().decrypt(password)
            logging.info(f'Decrypt: {res.path} --> {res.new_path}')
        except Exception as e:
            logging.error(f'{e}')


def traverse_ten(dir_path, head_size, type, password, remain_name, filter_suffix):
    matching_suffix = filter_suffix.split('|')
    if len(dir_path) <= 0:
        logging.error('You must input a dir_path path.')
    for p in dir_path:
        for sub_path in os.listdir(p):
            all_path = os.path.join(p, sub_path)
            if os.path.isdir(all_path):
                traverse_ten([all_path], head_size, type, password, remain_name, filter_suffix)
            else:
                if sub_path.split('.')[-1] in matching_suffix:
                    try:
                        if remain_name:
                            EncryptWriter(all_path).create_encrypt_info(head_size, type, password).encrypt()
                            logging.info(f'Encrypt: {p}')
                        else:
                            res = EncryptWriter(all_path).create_encrypt_info(head_size, type, password).encrypt_with_name()
                            logging.info(f'Encrypt: {p} --> {res.new_name}')
                    except Exception as e:
                        logging.error(f'{e}')


@main.command(help="Traverse dirs and encrypt the matching files")
@click.argument('dir_path', type=click.Path(exists=True), nargs=-1)
@click.option('-t', '--type', default=None, type=click.Choice(list(encrypt_str_map.keys())),
              help="加密方式：no为无密钥加密，rc4为有密钥加密")
@click.option('-h', '--head_size', default=1024, type=IntOrStrType(), help="待加密文件头大小")
@click.option('-p', '--password', hide_input=True, confirmation_prompt=True, default='',
              help="加密密钥，若不指定则默认no加密方法，指定则默认为rc4方法")
@click.option('--remain_name', is_flag=True,
              help="是否对文件名进行加密，默认加密，若不加密则指定--without-name")
@click.option('-f', '--filter_suffix', default='mp4|jpg|png|mov|jpeg|ts',
              help="文件后缀名，用`|`进行分割")
def ten(dir_path, head_size, type, password, remain_name, filter_suffix):
    traverse_ten(dir_path, head_size, type, password, remain_name, filter_suffix)


def traverse_tde(path, password, filter_suffix):
    matching_suffix = filter_suffix.split('|')
    if len(path) <= 0:
        logging.error('You must input a dir_path path.')
    for p in path:
        for sub_path in os.listdir(p):
            all_path = os.path.join(p, sub_path)
            if os.path.isdir(all_path):
                traverse_tde([all_path], password, filter_suffix)
            else:
                if sub_path.split('.')[-1] in matching_suffix:
                    try:
                        res = DecryptWriter(all_path).parse_decrypt_info().decrypt(password)
                        logging.info(f'Decrypt: {res.path} --> {res.new_path}')
                    except Exception as e:
                        logging.error(f'{e}')

@main.command(help="Traverse dirs and Decrypt the matching files")
@click.argument('path', type=click.Path(exists=True), nargs=-1)
@click.option('-p', '--password', hide_input=True, confirmation_prompt=True, default='',
              help="解密密钥")
@click.option('-f', '--filter_suffix', default='hep',
              help="文件后缀名，用`|`进行分割")
def tde(path, password, filter_suffix):
    traverse_tde(path, password, filter_suffix)


if __name__ == '__main__':
    main()
