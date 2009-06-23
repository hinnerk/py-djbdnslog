#!/usr/bin/env python

import djbdnslog, sys
from djbdnslog.scripts import check_args

def format_output(filename):
    for e in djbdnslog.parse_file(filename):
        print ("%(date)s  %(ip)s  %(port)s  %(id)s  %(status)14s  %(code)-5s  %(name)s"
               " %(name)s") % {'date': e[0].isoformat(),
                               'ip': ".".join(["%03d" % x for x in e[1]]),
                               'port': "%6d" % e[2],
                               'id': e[3],
                               'status': e[4],
                               'code': e[5],
                               'name': e[6],}


def main(argv):
    # check command line args
    check_args(argv)
    format_output(argv[1])


if __name__ == '__main__':
    main(sys.argv)