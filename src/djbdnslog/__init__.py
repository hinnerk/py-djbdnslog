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

def __hex2int(h):
    """ returns integer from hex string
    
    Example
        >>> _hex2int("a3")
        163
    """
    return int(h, 16)

def __translate_ip(ip_hex):
    """ returns a tuple of integers from a 8 char hex string.
    
    Example
        >>> translate_ip("a31c7110")
        (163, 28, 113, 16)
    """
    ip = (ip_hex[0:2], ip_hex[2:4], ip_hex[4:6], ip_hex[6:8])
    return tuple(map(lambda x:int(x,16), ip))

__code_lookup = {"+": "response",
               "-": "dropped",
               "I": "not implemented",
               "C": 'not "IN" class',
               "/": "defect/dropped"}

__type_lookup = {"0001":  "A",
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
        (datetime.datetime(2009, 6, 12, 11, 16, 25), (163, 28, 113, 16), 42714, '0795', 'response', 'MX ', 'leela.toppoint.de')
    """
    # line[1:26]     # date
    # line[26:34]    # IP Address
    # line[35:39]    # PORT
    # line[40:44]    # ID
    # line[45]       # code
    # line[47:51]    # type
    # line[52:]      # name
    
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
