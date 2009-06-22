import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "djbdnslog",
    version = "0.2",
    url = 'http://bitbucket.org/hinnerk/py-djbdnslog/',
    license = 'BSD',
    description = "Parses djbdns log files and returns native python data types.",
    long_description = read('README.rst'),

    author = 'Hinnerk Haardt',
    author_email = 'hinnerk@randnotizen.de',

    packages = find_packages('djbdnslog'),
    package_dir = {'': 'djbdnslog'},
    
    install_requires = ['setuptools', 'tai64n'],

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Other/Nonlisted Topic',
    ]
)