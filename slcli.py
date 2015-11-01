#!/usr/bin/python
#we use print("") instead of print"" for two reasons:
    #both work on 2.6? & 2.7 as well as 3.x
    #minimise later potential refactoring for 3.x
debug_printing = True
    #toggle for various debug output
import sys
    #is needed to read arguments
import envchecks
    #pre-req's / python env checks

def main(argv):
    if not envchecks.args_check_suceed():
        sys.exit(1)
    else:
        if debug_printing: print("envchecks suceeded...")


if __name__ == "__main__":
   main(sys.argv[1:])
