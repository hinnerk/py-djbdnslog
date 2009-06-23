import sys

def check_args(argv):
    if len(argv) != 2:
        print ("Help:\n"
               "%s filename.log"
               "filename.log = name of logfile")  % argv[0]
        sys.exit(1)
