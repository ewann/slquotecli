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
        import funcs_fs #functions specific to local fs interaction

        client = funcs_sl.conn_obj()
            #get a connection object
        import pprint
        pp = pprint.PrettyPrinter(indent=4)

        user_wants_to_exit = False
        next_order_container_id = 0
        while user_wants_to_exit == False:
            choice = funcs_cli_menu.main()
            if debug_printing: print (choice)
            if choice == 0:
                user_wants_to_exit = True
            elif choice == 1:
                print ("Connecting to SoftLayer...")
                pp.pprint(funcs_sl.list_all_quotes(client))
            elif choice == 2:
                quoteID = funcs_cli_menu.download_quote_pdf()
                print ("Connecting to SoftLayer...")
                quotePDF = funcs_sl.download_quote_pdf(client, quoteID)
                print ("Writing output file ")
                funcs_fs.pdfPickle(quoteID, quotePDF)
            elif choice == 3:
                print ("Connecting to SoftLayer...")
                pp.pprint(funcs_sl.list_all_product_packages(client))
            elif choice == 4:
                quoteID = funcs_cli_menu.reverify_existing_quote()
                print ("Connecting to SoftLayer...")
                quote_container = funcs_sl.get_existing_quote_container(client, quoteID)
                pp.pprint(funcs_sl.verify_quote_or_order(client, quote_container))
            elif choice == 5:
                quoteID = funcs_cli_menu.duplicate_existing_quote()
                print ("Connecting to SoftLayer...")
                quote_container = funcs_sl.get_existing_quote_container(client, quoteID)
                pp.pprint(funcs_sl.place_quote(client, quote_container))
            elif choice == 6:
                quoteID = funcs_cli_menu.create_order_cart()
                print ("Connecting to SoftLayer...")
                quote_container = funcs_sl.get_existing_quote_container(client, quoteID)
                pp.pprint(funcs_sl.create_order_cart(client, quote_container))
            elif choice == 7:
                packageID = funcs_cli_menu.list_product_package_required_options()
                print ("Connecting to SoftLayer...")
                pp.pprint(funcs_sl.list_product_package_options(client, packageID, True))
            elif choice == 8:
                print ("Connecting to SoftLayer...")
                pp.pprint(funcs_sl.get_datacenter_locations(client))
            elif choice == 9:
                print ("Connecting to SoftLayer...")
                pp.pprint(funcs_sl.get_location_groups(client))
            elif choice == 10:
                locationGroupID = funcs_cli_menu.get_location_group_members()
                print ("Connecting to SoftLayer...")
                pp.pprint(funcs_sl.get_location_group_members(client, locationGroupID))
            elif choice == 11:
                groupID = funcs_cli_menu.get_location_group_type()
                print ("Connecting to SoftLayer...")
                pp.pprint(funcs_sl.get_location_group_type(client,groupID))
            elif choice == 12:
                locationID = funcs_cli_menu.get_is_member_of_location_groups()
                print ("Connecting to SoftLayer...")
                pp.pprint(funcs_sl.get_is_member_of_location_groups(client,locationID))
            elif choice == 13:
                packageID = funcs_cli_menu.list_product_package_all_options()
                print ("Connecting to SoftLayer...")
                pp.pprint(funcs_sl.list_product_package_options(client, packageID, False))
            elif choice == 14:
                funcs_cli_menu.manage_quotes_menu(client, 0)

if __name__ == "__main__":
   main(sys.argv[1:])
