#!/usr/bin/python
#
#prerequisite is that:
#export SL_USERNAME=YOUR_USERNAME
#export SL_API_KEY=YOUR_API_KEY
#is in place
#
import SoftLayer
#increase default timeout to reduce false failure
#on slow or conjested connections
client = SoftLayer.create_client_from_env(timeout=240)
#
import pprint

import sys, getopt, os

enable_debug = True

def main(argv):
   inputfile = ''
   outputfile = ''
   if len(sys.argv) > 1:
       if enable_debug: print 'Number of arguments:', len(sys.argv), 'arguments.'
       if enable_debug: print 'First argument:', str(sys.argv[1])
       try:
          opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
       except getopt.GetoptError:
          usage()
          sys.exit(1)
       for opt, arg in opts:
           if enable_debug: print args.count
           if opt in ('-h', '--h'):
               usage()
               sys.exit(0)
           elif opt in ("-o", "--option"):
                if arg == "ai":
                    account_info()
                elif arg =="q":
                    quote()
   else:
        usage()
        if enable_debug: print "no arguments detected"
        sys.exit(2)

def account_info():
    pp = pprint.PrettyPrinter(indent=4)
    return pp.pprint(client['Account'].getObject())

def quote():
    #order =
    #client['SoftLayer_Billing_Order_Quote'].placeQuote()


    pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(client['SoftLayer_Billing_Order'].getAllObjects())

    #client['SoftLayer_Product_Order'].placeQuote()
    hwOptions = client['Hardware'].getCreateObjectOptions()
    pp.pprint(hwOptions)

    locations = client['SoftLayer_Location'].getDatacenters()
    pp.pprint(locations)


#pp(result)

#https://gist.github.com/underscorephil/4587027
#https://gist.github.com/underscorephil/4732131
#https://gist.github.com/underscorephil/5861119


def usage():
    print
    print 'Usage:'
    print 'process.py -o <option>'
    print 'Or:'
    print 'python process.py -o <option'
    print
    print 'Depending on your environment configuration.'

if __name__ == "__main__":
   main(sys.argv[1:])
