#!/usr/bin/env python

import djbdnslog, sys
from djbdnslog.scripts import check_args

def format_output(filename):
    for e in djbdnslog.parse_file(filename):
        print "%s  %-15s  %0d  %s  %14s  %-5s  %s" % e


def main(argv):
    # check command line args
    check_args(argv)
    format_output(argv[1])


if __name__ == '__main__':
    main(sys.argv)