import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "djbdnslog",
    version = "0.2.3",
    url = 'http://bitbucket.org/hinnerk/py-djbdnslog/',
    license = 'BSD',
    description = "Parses djbdns log files and returns native python data types.",
    long_description = read('README'),

    author = 'Hinnerk Haardt',
    author_email = 'hinnerk@randnotizen.de',

    package_dir = {'': 'src'},
    packages = ['djbdnslog'],
    
    entry_points = {
        "console_scripts": [
            'stats = djbdnslog.scripts.stats:main',
            'convert = djbdnslog.scripts.convert:main',
        ]
    },
    
    #scripts = ['src/bin/stats.py', 'src/bin/convert.py'],
    install_requires = ['setuptools', 'tai64n'],

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Other/Nonlisted Topic',
    ],
)