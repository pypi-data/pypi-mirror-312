import os
import subprocess

from setuptools import setup, find_packages


try:
    with open(os.path.join(os.path.split(__file__)[0], "readme.md"), "r", encoding='utf8') as fh:
        long_description = fh.read()
except Exception:
    long_description = subprocess.run(["curl", 'https://raw.githubusercontent.com/lichunown/head-encrypt/master/readme.md'],
                                      capture_output=True, text=True, encoding='utf8').stdout


setup(
    name='headecpt',
    version="0.1.3",
    author="lcy",
    author_email="lichunyang_1@outlook.com",
    description="encrypt/decrypt file header for simple and quick encrypt/decrypt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lichunown/head-encrypt.git",

    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
        "Topic :: File Formats",
    ],

    packages=find_packages(),
    data_files=[],
    install_requires=[
        'click',
    ],
    extras_require={
        'crypto': ['pycryptodome'],
    },

    entry_points={'console_scripts': [
       'headecpt = headecpt.main:main',
    ]},

    zip_safe=False
)