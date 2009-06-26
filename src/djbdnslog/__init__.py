"""
module to parse djbdns log entries (or files)

Module Functions
================

parse_line(line)
    returns a tuple from one log entry

parse_file(filename)
    yields tuples from a log file

simple_statistics(filename)
    returns a simple statistic from a log file

"""

import tai64n

class DJBDNSlogDecodeError(Exception):
    pass


def __hex2int(h):
    """ returns integer from hex string
    
    Example
        >>> __hex2int("a3")
        163
    """
    return int(h, 16)


def __translate_ip(ip):
    """ returns a tuple of integers from a 8 or 32 char hex string.

    Args
        ip: string, hex-encoded IPv4 or IPv6 address

    Returns
        a tuple containing either 4 or 8 integers
    
    Examples
        >>> __translate_ip("a31c7110")
        (163, 28, 113, 16)
        >>> __translate_ip("7f000001")
        (127, 0, 0, 1)
        >>> __translate_ip("00000000000000000000ffff7f000001")
        (0, 0, 0, 0, 0, 65535, 32512, 1)
    """
    l = max((2, len(ip) / 8))                       # 2 for IPv4, 4 for IPv6
    ip_hex = (ip[l*i:l*i+l] for i in xrange(l*2))   # split in l-length strings
    return tuple(map(lambda x:int(x,16), ip_hex))   # return tuple containing int

__code_lookup = {"+": "response",
               "-": "dropped",
               "I": "not implemented",
               "C": 'not "IN" class',
               "/": "defect/dropped"}

__type_lookup = {   # see here for more:
                    # http://www.iana.org/assignments/dns-parameters
               "0001":  "A",
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
               "00ff": 	"*"}


def parse_line(line, t64n=tai64n.decode_tai64n,
                     translate_ip=__translate_ip,
                     hex2int=__hex2int,
                     code_dict=__code_lookup,
                     type_dict=__type_lookup):
    """ returns tuple of decoded data from a single log line
    Args
        line            one log entry
        [everything else is optional]
        t64n            callable, decodes TAI64n external
        translate_ip    callable, decodes IPv4 hex string
        hex2int         callable, decodes hex string
        code_dict       dict, {"I": "not implemented",...}
        type_dict       dict, {"00fc": 	"AXFR",...}
    
    Returns
        A tuple containing the decoded data. Decoding depends on the
        given decoders, the default ones are:
            timestamp   => datetime.datetime
            IPv4        => (int, int, int, int)
            PORT        => int
            ID          => string
            CODE        => dict lookup (see module source, __code_lookup)
            TYPE        => dict lookup (see module source, __type_lookup)
            NAME        => string
        
    Example
        >>> parse_line("@400000004a32392b2aa21dac a31c7110:a6da:0795 + 000f leela.toppoint.de")
        (datetime.datetime(2009, 6, 12, 11, 16, 25, 715267), (163, 28, 113, 16), 42714, '0795', 'response', 'MX ', 'leela.toppoint.de')
    """
    # line[1:26]     # date
    # line[26:34]    # IP Address
    # line[35:39]    # PORT
    # line[40:44]    # ID
    # line[45]       # code
    # line[47:51]    # type
    # line[52:]      # name
    try:
        date, stuff, code, type, name = line.split()
    except ValueError:
        try:
            # possibly no date given?
            stuff, code, type, name = line.split()
            date = None
        except:
            raise DJBDNSlogDecodeError("Can't decode Entry: '%s'" % line)
    ip, port, id = stuff.split(":")
    if date: # and date.startswith("@"):
        date.strip("@")
        date = t64n(date[1:])
    return (date, translate_ip(ip), hex2int(port), id, code_dict.get(code, "UNKNOWN"),
            type_dict.get(type, "UNKNOWN"), name)


def parse_file(filename):
    """ yields tuple of entries for every line
    """
    for line in open(filename).readlines():
        yield parse_line(line)


def simple_statistics(filename):
    ips = {}
    codes = {}
    types = {}
    names = {}
    for d in parse_file(filename):
            ips[d[1]] = ips.get(d[1], 0) + 1
            codes[d[4]] = codes.get(d[4], 0) + 1
            types[d[5]] = types.get(d[5], 0) + 1
            names[d[6]] = names.get(d[6], 0) + 1
    return {'ips': ips,
            'codes': codes,
            'types': types,
            'names': names}


if __name__ == '__main__':
    import doctest
    doctest.testmod()
