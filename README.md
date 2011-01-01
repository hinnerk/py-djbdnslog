=========
djbdnslog
=========

A python-module to parse DJBDNS log files.


Home URL: http://bitbucket.org/hinnerk/py-djbdnslog/

TODO / Things that do not work (yet)
====================================

In no particular order:

* resolve IP adresses
* IPv6 adresses (djbdns patch from fefe_)
* expand list of dns parameters_
* add more scripts
* extend ``stats`` script
* make format of the output of ``convert`` defineable
* make the stats dynamic

Please leave bugs, ideas, wishes, flames etc. at the bugtracker_.

.. _fefe: http://www.fefe.de/dns/
.. _bugtracker: http://bitbucket.org/hinnerk/py-djbdnslog/issues/
.. _parameters: http://www.iana.org/assignments/dns-parameters


Installation
============

This software has two faces:

1. There are ready to use scripts to convert djbdns log files to human readable format, get a statistical overview etc.
2. You can use the python module as a library in your own software.


1. Using the Scripts without system-wide installation
*****************************************************

I included a buildout setup to contain everything into one directory. Make sure you have python installed (installed by default on recent operating systems like FreeBSD, Linux, Mac OS X or OpenSolaris). Clone `the mercurial repository`__ or `download the .zip archive`__. Then run::

    python ./bootstrap.py
    ./bin/buildout

If everything went fine you should find the scripts in ``./bin`` (try ``./bin/convert <yourlogfile.log>`` to see a human readable dump of your log file).

__ http://bitbucket.org/hinnerk/py-djbdnslog/
__ http://bitbucket.org/hinnerk/py-djbdnslog/get/tip.zip


2. Installing the Python Module
*******************************

If you are using a software that depends on djbdnslog, it should get installed automatically. If you develop your own software against djbdnslog, add this to the setup.py of you software::

        install_requires = ['setuptools', 'djbdnslog'],

And whatever tool you use for development (zc.buildout, to name one example) will fetch it for you, so you can simply ``import djbdnslog`` in your code.


=====
Usage
=====

Scripts
=======

``convert logfile.log``
***********************

Dumps the content of a log file to stdout::

    $ ./bin/convert test.log
        [human readable log data]

The dumped format is hard coded in the source, I'm sorry, but that's the way it is.


``stats logfile.log``
*********************

returns statistical data of the content of a log file to stdout::

    $ ./bin/stats test.log
        [statistical data]

The statics is hard coded in the source, again I'm sorry for that.


Module Functions
================

``parse_line(line)``
    parses a single log entry (usually a line) and returns a tuple containing python base data types. Converter functions may optionally be specified.
``parse_file(filename)``
    Does the same parse_line does except it tases a file name as argument. Converter functions can not be specified.
``simple_statistics(filename)``
    Creates a simple statistic from a log file.


That's it, folks!