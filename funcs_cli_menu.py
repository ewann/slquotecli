import class_obj
    #called from manage_quotes_menu
def main():
    print ("")
    print ("")
    print ("Press the number then <enter> for the option you want:")
    print ("")
    print ("  1 - Show all quotes in the account")
    print ("  2 - Download PDF for a specific quote")
    print ("  3 - List all (Active) SoftLayer_Product_Package(s)")
    print ("  4 - Re-verify existing quote")
    print ("  5 - Duplicate existing quote")
    print ("  6 - <BROKEN?> Create Order Cart")
    print ("  7 - List SoftLayer_Product_Package required options for a given package")
    print (" 13 - List SoftLayer_Product_Package all options for a given package")
    print ("  8 - List Location_DataCenter (DC locations)")
    print ("  9 - List Location_Group(s)")
    print (" 10 - List Location_Group members")
    print (" 11 - List type of a Location_Group")
    print (" 12 - List Location_Group(s) location is member of")
    print (" 14 - Manage Quotes")
    print ("  0 - Exit")
    user_input = raw_input("Your choice: ")
    try:
        return int(user_input)
    except:
        main()

def download_quote_pdf():
    print ("")
    print ("")
    print ("Enter the id for the quote you wish to download:")
    user_input = raw_input("id: ")
    return int(user_input)

def reverify_existing_quote():
    print ("")
    print ("")
    print ("Enter the id for the quote you wish to re-verify:")
    user_input = raw_input("id: ")
    return int(user_input)

def duplicate_existing_quote():
    print ("")
    print ("")
    print ("Enter the id for the existing quote you wish to duplicate:")
    user_input = raw_input("id: ")
    return int(user_input)

def create_order_cart():
    print ("")
    print ("")
    print ("Enter the id for the source quote you wish to cart-ify:")
    user_input = raw_input("id: ")
    return int(user_input)

def list_product_package_required_options():
    print ("")
    print ("")
    print ("Enter the SoftLayer_Product_Package id for which you")
    print ("would like to see the required options:")
    user_input = raw_input("id: ")
    return int(user_input)

def list_product_package_all_options():
    print ("")
    print ("")
    print ("Enter the SoftLayer_Product_Package id for which you")
    print ("would like to see all options:")
    user_input = raw_input("id: ")
    return int(user_input)

def get_location_group_members():
    print ("")
    print ("")
    print ("Enter the location id for which you")
    print ("would like to see its Location_Group membership:")
    user_input = raw_input("id: ")
    return int(user_input)

def get_location_group_type():
    print ("")
    print ("")
    print ("Enter the location id for which you")
    print ("would like to see its Location_Group type:")
    user_input = raw_input("id: ")
    return int(user_input)

def get_is_member_of_location_groups():
    print ("")
    print ("")
    print ("Enter the location id for which you")
    print ("would like to see its Location_Group membership:")
    user_input = raw_input("id: ")
    return int(user_input)

def manage_quotes_menu(client, datacenterID):
    def get_datacenter_id():
        print ("")
        print ("")
        print ("Enter the datacenter id for which you")
        print ("would like to build a quote:")
        user_input = raw_input("Your choice: ")
        try:
            return int(user_input)
        except:
            get_datacenter_id()
    print ("")
    print ("vars in this context:")
    print client
    print datacenterID
    print ("")
    print ("  1 - Specify datacenter")
    print ("  2 - List existing quote container(s)")
    print ("  8 - List existing product container(s)")
    print ("  3 - Create a product container")
    print ("  4 - Modify a product container")
    print ("  5 - Delete a product container")
    print ("  6 - Verify a quote (all existing product containers)")
    print ("  7 - Place a quote (all existing product containers)")
    print ("  0 - Back to main menu (throw away unsaved work)")
    user_input = raw_input("Your choice: ")
    try:
        choice = int(user_input)
    except:
        manage_quotes_menu(client)
    if choice == 0:
        return
    elif choice == 1:
        datacenterID = get_datacenter_id()
        manage_quotes_menu(client, datacenterID)
    elif choice == 2:
        print ("")
        print ("Listing quote containers...")
        class_obj.list_objects_of_type(class_obj.order_container)
        print ("Finished listing quote containers.")
        print ("")
        manage_quotes_menu(client, datacenterID)
    elif choice == 8:
        print ("")
        print ("Listing product containers...")
        class_obj.list_objects_of_type(class_obj.order_container)
        print ("Finished listing product containers.")
        print ("")
        manage_quotes_menu(client, datacenterID)
    elif choice == 3:
        user_input = raw_input("Enter an asci containerIdentifier (friendly name): ")
        my_oc = {}
        my_oc['complexType'] = 'SoftLayer_Container_Product_Order_Hardware_Server'
        my_oc['quantity'] = 1
        my_oc['hardware'] = 1#[hw_container.returnSelf()]
        my_oc['containerIdentifier'] = user_input
        my_oc['packageId'] = '248'
        my_oc['prices'] = 1#price_container.returnSelf()
            #prices doesn't need [] because of datatype?
        my_oc['location'] = '449596'
        container = class_obj.product_container(my_oc)

        class_obj.list_objects_of_type(class_obj.order_container)
        manage_quotes_menu(client, datacenterID)
