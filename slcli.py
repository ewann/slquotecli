#!/usr/bin/python
#we use print("") instead of print"" for two reasons:
    #both work on 2.6? & 2.7 as well as 3.x
    #minimise later potential refactoring for 3.x    
import sys
    #is needed to read arguments
import envchecks
    #pre-req's / python env checks

def main(argv):
    if not envchecks.args_check_suceed():
        sys.exit(1)
    else:
        print("hi")
        print "low"


if __name__ == "__main__":
   main(sys.argv[1:])
