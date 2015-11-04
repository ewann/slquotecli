#menu code based on the example at:
#http://codereview.stackexchange.com/questions/65305/making-user-menus-in-a-text-based-game

class State:
    def __init__(self, starting_loc):
        self.alive = True
        self.location = starting_loc
        self.locations = {}
        #state for slquotecli goes here?
        import pprint
        self.pp = pprint.PrettyPrinter(indent=4)
        self.slclient = funcs_sl.conn_obj()
        self.list_sl_dc = []
        self.list_sl_active_product_packages = []
        self.master_dict = {}
        self.wip_dict = {}
        self.wip_dict['complexType'] = 'SoftLayer_Container_Product_Order_Hardware_Server'
        self.wip_dict['quantity'] = 1
        self.num_order_containers = 0
        self.num_product_containers = 0
    def addloc(self, location):
        self.locations[location.name] = location
    def gotoloc(self, locname):
        self.location = self.locations[locname]
    def populate_list_sl_dc(self, dclist):
        self.list_sl_dc = dclist
    def populate_list_active_product_packages(self, pplist):
        self.list_sl_active_product_packages = pplist

class Location:
    def __init__(self, name, desc, options=None):
        self.name = name
        self.desc = desc
        self.options = options
    def start(self):
        print self.desc
    def print_opts(self):
        if(self.options != None):
            for i in range(len(self.options)):
                print "  {0}. {1}".format(i, self.options[i].text)
    def get_choice(self, state):
        choice = raw_input("> ")
        print "You chose \"{0}\"".format(choice)
        try:
            index = int(choice)
            self.options[index].action.execute(state)
            return True
        except Exception as e:
            print(e)
            print("Please choose a valid option")
            return False

class Option:
    def __init__(self, text, action):
        self.text = text
        self.action = action

class GoToLocation:
    def __init__(self, location):
        self.loc = location
    def execute(self, state):
        state.gotoloc(self.loc)
        state.location.start()

class CloseDown:
    def __init__(self, message):
        self.message = message
    def execute(self, state):
        state.alive = False
        print(self.message)

class Message:
    def __init__(self, msg):
        self.msg = msg
    def execute(self, state):
        print self.msg

class OptionMutator:
    def __init__(self, location, index, newoption):
        self.locname = location
        self.index = index
        self.newoption = newoption
    def execute(self, state):
        loc = state.locations[self.locname]
        if(self.index < 0 or self.index >= len(loc.options)):
            loc.options.append(self.newoption)
        else:
            loc.options[self.index] = self.newoption

class MultiAction:
    def __init__(self, actions=None):
        self.actions = actions
    def execute(self, state):
        if(self.actions == None): return
        for action in self.actions:
            action.execute(state)

'''
duplicate for removal? 20151104 19.42 - several runs without finding an issue caused by this
class SpecifyDatacenter:
    def execute(self, state):
        print ("Specify datacenter id")
        choice = raw_input("> ")
        print ("You chose \"{0}\"").format(choice)
        state.wip_dict['location'] = int(choice)
'''

class DownloadQuotePdf:
    def execute(self, state):
        print ("Specify quote id")
        choice = raw_input("> ")
        print ("You chose \"{0}\"").format(choice)
        quoteID = int(choice)
        print ("Downloading Pdf...")
        print ("")
        try:
            quoteObj = funcs_sl.download_quote_pdf(state.slclient, quoteID)
        except Exception,e:
            print ("")
            print ("failed with error")
            print (str(e))
        print ("")
        print ("Saving Pdf...")
        try:
            result = funcs_fs.pdfPickle(quoteID, quoteObj)
            print ("Saved quote: " + str(result) + " to local filesystem")
            print ("")
        except Exception,e: #print str(e)
            print ("Failed with error:")
            print (str(e))
            print ("")

class ReverifyExistingQuote:
    def execute(self, state):
        print ("Enter the id of the quote you wish to re-verify:")
        choice = raw_input("> ")
        print ("You chose \"{0}\"").format(choice)
        quoteID = int(choice)
        print ("Connecting to SoftLayer...")
        print ("")
        try:
            state.pp.pprint(funcs_sl.verify_quote_or_order(state.slclient, funcs_sl.get_existing_quote_container(state.slclient, quoteID)))
            print ("")
        except Exception,e:
            print ("Failed with error:")
            print (str(e))
            print ("")

class DuplicateExistingQuote:
    def execute(self, state):
        print ("Enter the id of the source quote you wish to duplicate:")
        choice = raw_input("> ")
        print ("You chose \"{0}\"").format(choice)
        quoteID = int(choice)
        print ("Connecting to SoftLayer...")
        print ("")
        try:
            state.pp.pprint(funcs_sl.place_quote(state.slclient, funcs_sl.get_existing_quote_container(state.slclient, quoteID)))
            print ("")
        except Exception,e:
            print ("Failed with error:")
            print (str(e))
            print ("")

class ShowAllQuotes:
    def execute(self, state):
        print ("Connecting to SoftLayer")
        print ("")
        try:
            state.pp.pprint(funcs_sl.list_all_quotes(state.slclient))
            print ("")
        except Exception,e:
            print ("Failed with error:")
            print (str(e))
            print ("")

class ShowAllProductPackages:
    def __init__(self, active=False, clioutput=False):
        self.active = active
        self.clioutput = clioutput
    def execute(self, state):
        if state.list_sl_active_product_packages:
            print ("Found data in local cache, using that")
            if self.clioutput:
                state.pp.pprint(state.list_sl_active_product_packages)
                print ("")
        else:
            print ("Nothing found in local cache...")
            print ("Connecting to SoftLayer...")
            print ("")
            try:
                result = funcs_sl.list_all_product_packages(state.slclient, self.active)
                state.pp.pprint(result)
                state.populate_list_active_product_packages(result)
                print ("")
            except Exception,e:
                print ("Failed with error:")
                print (str(e))
                print ("")

class ListPackageOptions:
    def __init__(self, required=False):
        self.required = required
    def execute(self, state):
        print ("Enter the SoftLayer_Product_Package id:")
        choice = raw_input("> ")
        print ("You chose \"{0}\"").format(choice)
        packageID = int(choice)

        #if we find the package in self.master_dict = {}
            #use the cache
        #else
            # look it up, and store it

        print ("Connecting to SoftLayer...")
        print ("")
        try:
            state.pp.pprint(funcs_sl.list_product_package_options(state.slclient, packageID, self.required))
            print ("")
        except Exception,e:
            print ("Failed with error:")
            print (str(e))
            print ("")

class GetDataCenterLocations:
    def __init__(self, clioutput=False):
        self.clioutput = clioutput
    def execute(self, state):
        if state.list_sl_dc:
            print ("Found data in local cache, using that")
            print ("")
            if self.clioutput:
                state.pp.pprint(state.list_sl_dc)
                print ("")
        else:
            print ("Nothing found in local cache...")
            print ("Connecting to SoftLayer...")
            print ("")
            try:
                result = funcs_sl.get_datacenter_locations(state.slclient)
                if self.clioutput:
                    state.pp.pprint(result)
                state.populate_list_sl_dc(result)
                print ("")
            except Exception,e:
                print ("Failed with error:")
                print (str(e))
                print ("")

class GetLocationGroups:
    def execute(self, state):
        print ("Connecting to SoftLayer...")
        print ("")
        try:
            state.pp.pprint(funcs_sl.get_location_groups(state.slclient))
            print ("")
        except Exception,e:
            print ("Failed with error:")
            print (str(e))
            print ("")

class GetLocationGroupMembers:
    def execute(self, state):
        print ("Enter the SoftLayer_Location_Group id:")
        choice = raw_input("> ")
        print ("You chose \"{0}\"").format(choice)
        locationGroupID = int(choice)
        print ("Connecting to SoftLayer...")
        print ("")
        try:
            state.pp.pprint(funcs_sl.get_location_group_members(state.slclient, locationGroupID))
            print ("")
        except Exception,e:
            print ("Failed with error:")
            print (str(e))
            print ("")

class GetLocationGroupType:
    def execute(self, state):
        print ("Enter the SoftLayer_Location_Group id:")
        choice = raw_input("> ")
        print ("You chose \"{0}\"").format(choice)
        locationGroupID = int(choice)
        print ("Connecting to SoftLayer...")
        print ("")
        try:
            state.pp.pprint(funcs_sl.get_location_group_type(state.slclient, locationGroupID))
            print ("")
        except Exception,e:
            print ("Failed with error:")
            print (str(e))
            print ("")

class GetIsMemberOfLocationGroups:
    def execute(self, state):
        print ("Enter the SoftLayer_Location id:")
        choice = raw_input("> ")
        print ("You chose \"{0}\"").format(choice)
        locationID = int(choice)
        print ("Connecting to SoftLayer...")
        print ("")
        try:
            state.pp.pprint(funcs_sl.get_is_member_of_location_groups(state.slclient, locationID))
            print ("")
        except Exception,e:
            print ("Failed with error:")
            print (str(e))
            print ("")

menu_main = Location("menu_main",
    "Press the number then <enter> for the option you want:",
    [Option("Download Quote Pdf for a specific quote", DownloadQuotePdf()),
    Option("(MENU) Manage Quotes", GoToLocation("menu_manage_quotes")),
    Option("Re-verify existing quote on control portal", ReverifyExistingQuote()),
    Option("Duplicate existing quote on control portal", DuplicateExistingQuote()),
    Option("<SL Not Imlemented> Create quote cart", Message("According to https://control.softlayer.com/support/tickets/23363617 (one of Ewan's accounts) regarding functionality: ['SoftLayer_Billing_Order_Cart'].createCart(container) 'the customer won't be able to create a cart, because this is a feature which is on hold'")),
    Option("Show all quotes in account", ShowAllQuotes()),
    Option("Show all active SoftLayer_product_Package(s)", ShowAllProductPackages(active=True, clioutput=True)),
    Option("List SoftLayer_Product_Package *required* options for a given package", ListPackageOptions(required=True)),
    Option("List SoftLayer_Product_Package *all* options for a given package", ListPackageOptions(required=False)),
    Option("List Location_DataCenter (DC locations)", GetDataCenterLocations(clioutput=True)),
    Option("List Location_Group(s)", GetLocationGroups()),
    Option("List Location_Group members", GetLocationGroupMembers()),
    Option("List type of a Location_Group",  GetLocationGroupType()),
    Option("List Location_Group(s) location is a member of", GetIsMemberOfLocationGroups()),
    Option("Exit to shell", CloseDown("Goodbye."))])

class SpecifyDatacenter:
    def execute(self, state):
        if not state.list_sl_dc:
            print "Local cache doesn't contain datacenter data, fixing that..."
            GetDataCenterLocations(False).execute(state)
        print ("List of valid datacenter's currently cached:")
        state.pp.pprint(state.list_sl_dc)
        print ("Specify datacenter id:")
        choice = raw_input("> ")
        print ("You chose \"{0}\"").format(choice)
        state.wip_dict['location'] = int(choice)

class ShowDatacenter:
    def execute(self, state):
        print ("Currently selected datacenter is:")
        print state.wip_dict['location']

class ShowWipDict:
    def execute(self, state):
        print ("WIP dict for in progress quote looks like:")
        state.pp.pprint(state.wip_dict)

menu_manage_quotes = Location("menu_manage_quotes",
    "Press the number then <enter> for the option you want:",
    [Option("(MENU) Return to previous menu (nothing will be saved)", GoToLocation("menu_main")),
    Option("Show in progress quote", ShowWipDict()),
    Option("Specify datacenter", SpecifyDatacenter()),
    Option("Show currently selected datacenter", ShowDatacenter()),
    Option("List existing quote container(s)", Message("Not implemented")),
    Option("List existing product container(s)", Message("Not implemented")),
    Option("Create a product container", Message("Not implemented")),
    Option("Modify a product container", Message("Not implemented")),
    Option("Delete a product container", Message("Not implemented")),
    Option("Verify a quote (all existing product containers)", Message("Not implemented")),
    Option("Place a quote (all existing product containers)", Message("Not implemented")),
    Option("Exit to shell", CloseDown("Goodbye"))])

menu_example = Location("menu_example", """You want to take multiple actions,
or mutate menu items""",
                       [Option("Main Menu", GoToLocation("menu_main")),
                        Option("Multi-mutate",
                               MultiAction([Message("Mutating the menu!"),
                                            OptionMutator("menu_manage_quotes", 3, Option("Trapdoor", CloseDown("We exited. Trick or treat!")))]))])

if __name__=="__main__":
    import sys #needed to read cli arguments
    import funcs_env_checks #pre-req's / python env checks
    debug_printing = True #toggle for various debug output
    if not funcs_env_checks.args_check_suceed():
        sys.exit(1)
    else:
        if debug_printing: print("envchecks returned true...")
        import funcs_sl #functions that interact with SL api
        import funcs_fs #functions that interact with local filesystem
        s = State(menu_main)
        s.addloc(menu_main)
        s.addloc(menu_manage_quotes)
        s.location.start()

        while(s.alive):
            s.location.print_opts()
            s.location.get_choice(s)
