#!/usr/bin/env python

"""
parses djbdns log files

line[1:26]     # date
line[26:34]    # IP Address
line[35:39]    # PORT
line[40:44]    # ID
line[45]       # code
line[47:51]    # type
line[52:]      # name


"""

import tai64

def _hex2int(h):
    """ returns integer from hex string
    
    Example
        >>> _hex2int("a3")
        163
    """
    return int(h, 16)

def _translate_ip(ip_hex):
    """ returns a tuple of integers from a 8 char hex string.
    
    Example
        >>> translate_ip("a31c7110")
        (163, 28, 113, 16)
    """
    ip = (ip_hex[0:2], ip_hex[2:4], ip_hex[4:6], ip_hex[6:8])
    return tuple(map(lambda x:int(x,16), ip))

_code_lookup = {"+": "response",
               "-": "dropped",
               "I": "not implemented",
               "C": 'not "IN" class',
               "/": "defect/dropped"}

_type_lookup = {"0001":  "A",
               "0002": 	"NS",
               "0005": 	"CNAME",
               "0006": 	"SOA",
               "000c": 	"PTR",
               "000f": 	"MX ",
               "0010": 	"TXT",
               "001c": 	"AAAA",
               "0026": 	"A6 ",
               "00fb": 	"IXFR",
               "00fc": 	"AXFR",
               "00ff": 	"wildcard"}


def __metacall(clble, arg):
    if isinstance(clble, dict):
        return clble.get(arg, "UNKNOWN")
    return clble(arg)

def parse_line(line, t64n=tai64.decode_tai64n):
    """ returns tuple of entries from log line
    
    Example
        >>> parse_line("@400000004a32392b2aa21dac a31c7110:a6da:0795 + 000f leela.toppoint.de")
        (datetime.datetime(2009, 6, 12, 11, 16, 25), (163, 28, 113, 16), 42714, '0795', 'response', 'MX ', 'leela.toppoint.de')
    """
    if line.startswith("@"):
        date = t64n(line[1:25])
    else:
        date = None
    return (date,
            _translate_ip(line[26:34]),  # IP Address
            _hex2int(line[35:39]),      # PORT
            line[40:44],                # ID
            _code_lookup.get(line[45], "UNKNOWN"),      # code
            _type_lookup.get(line[47:51], "UNKNOWN"),   # type
            line[52:-1])                  # name


def parse_file(filename):
    """ yields tuple of entries for every line
    """
    for line in open(filename).readlines():
        yield parse_line(line)


if __name__ == '__main__':
    import doctest
    doctest.testmod()