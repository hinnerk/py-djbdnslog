#!/usr/bin/env python2.5

import djbdnslog


def count_values(filename):
    ips = {}
    codes = {}
    types = {}
    names = {}
    for d in djbdnslog.parse_file(filename):
            ips[d[1]] = ips.get(d[1], 0) + 1
            codes[d[4]] = codes.get(d[4], 0) + 1
            types[d[5]] = types.get(d[5], 0) + 1
            names[d[6]] = names.get(d[6], 0) + 1
    return {'ips': ips,
            'codes': codes,
            'types': types,
            'names': names}

