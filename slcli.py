#!/usr/bin/python
#Style: we use print("") instead of print"" for two reasons:
    #both work in 2.6? & 2.7 as well as 3.x
    #minimise later potential refactoring for 3.x
debug_printing = True #toggle for various debug output
import sys #needed to read cli arguments
import funcs_env_checks #pre-req's / python env checks

def main(argv):
    if not funcs_env_checks.args_check_suceed():
        sys.exit(1)
    else:
        if debug_printing: print("envchecks returned true...")
        import funcs_sl #functions specific to SL interaction
        import funcs_cli_menu #functions specific to providing a cli menu
        #import SoftLayer
        #increase default timeout to reduce false failure
        #on slow or conjested connections
        client = funcs_sl.conn_obj()

        import pprint
        pp = pprint.PrettyPrinter(indent=4)

        user_wants_to_exit = False

        while user_wants_to_exit == False:
            choice = funcs_cli_menu.main()
            if debug_printing: print (choice)
            if choice == 0:
                user_wants_to_exit = True
            elif choice == 1:
                print ("Connecting to SoftLayer...")
                pp.pprint(funcs_sl.all_quotes(client))
            elif choice == 2:
                quoteID = funcs_cli_menu.download_quote_pdf()
                mypdf = funcs_sl.download_quote_pdf(client, quoteID)
                pdfPickle(mypdf)
                #print ("Connecting to SoftLayer...")

def pdfPickle(bin_obj):
    import pickle
    pickleFileName = "out.pdf"
    pickleFile = open(pickleFileName, 'wb')
    pickle.dump(bin_obj, pickleFile, pickle.HIGHEST_PROTOCOL)
    pickleFile.close()



if __name__ == "__main__":
   main(sys.argv[1:])
