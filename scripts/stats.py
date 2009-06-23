#!/usr/bin/env python2.5

import djbdnslog, sys

if len(sys.argv) != 2:
    print ("Help:\n"
           "%s filename.log"
           "filename.log = name of logfile")  % sys.argv[0]
    sys.exit(1)

ergebnislisten = djbdnslog.count_values(sys.argv[1])

for liste in ergebnislisten:
    print "*** %s ***" % liste.upper()
    for entry in ergebnislisten[liste]:
        print "%22s:\t%2d" % (entry, ergebnislisten[liste][entry])
    print "\n"