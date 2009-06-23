#!/usr/bin/env python

import djbdnslog, sys
from djbdnslog.scripts import check_args


def print_statistics(filename):
    ergebnislisten = djbdnslog.simple_statistics(filename)
    for liste in ergebnislisten:
        print "*** %s ***" % liste.upper()
        for entry in ergebnislisten[liste]:
            print "%22s:\t%2d" % (entry, ergebnislisten[liste][entry])
        print "\n"
    

def main(argv):
    check_args(argv)
    print_statistics(argv[1])


if __name__ == '__main__':
    main(sys.argv)