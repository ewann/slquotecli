#!/usr/bin/python
import sys
    #is needed to read arguments
import envchecks
    #pre-req's / python env checks

def main(argv):
    if not envchecks.args_check_suceed():
        sys.exit(1)
        


if __name__ == "__main__":
   main(sys.argv[1:])
