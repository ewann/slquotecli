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
        self.cache_dict = {}
        self.wip_dict = {}
        self.wip_dict['complexType'] = 'SoftLayer_Container_Product_Order_Hardware_Server'
        self.wip_dict['quantity'] = 1
        self.num_order_containers = 0
        self.num_product_containers = 0
    def addloc(self, location):
        self.locations[location.name] = location
    def gotoloc(self, locname):
        self.location = self.locations[locname]
    #sl datastructures
    def overwrite_cache_dict_key(self, rootkey, content):
        self.cache_dict[rootkey] = content

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
        if 'sl-product-packages' in state.cache_dict:
            print ("Found data in local cache, using that")
            if self.clioutput:
                state.pp.pprint(state.cache_dict['sl-product-packages'])
                print ("")
        else:
            print ("Nothing found in local cache...")
            print ("Connecting to SoftLayer...")
            print ("")
            try:
                result = funcs_sl.list_all_product_packages(state.slclient, self.active)
                state.pp.pprint(result)
                state.overwrite_cache_dict_key('sl-product-packages', result)
                print ("")
            except Exception,e:
                print ("Failed with error:")
                print (str(e))
                print ("")

class ListPackageOptions:
    def __init__(self, required=False):
        self.required = required
    def execute(self, state):
        if debug_printing: print ("self.required: "+str(self.required))
        print ("Enter the SoftLayer_Product_Package id:")
        choice = raw_input("> ")
        print ("You chose \"{0}\"").format(choice)
        packageID = int(choice)
        config_key_name = 'sl-pkg-'+str(packageID)+'-configs'
        price_key_name = 'sl-pkg-'+str(packageID)+'-prices'
        if config_key_name in state.cache_dict and price_key_name in state.cache_dict:
            print ("Found data in local cache, using that")
            BuildProductOptions.execute(BuildProductOptions(), state, state.cache_dict[config_key_name], state.cache_dict[price_key_name], packageID, self.required)
        else:
            #we need to populate both sets of values
            print ("Nothing found in local cache...")
            print ("Connecting to SoftLayer...")
            print ("")
            try:
                result = funcs_sl.get_configurations(state.slclient, packageID)
                state.overwrite_cache_dict_key(config_key_name, result)
                result = funcs_sl.get_prices(state.slclient, packageID)
                state.overwrite_cache_dict_key(price_key_name, result)
                BuildProductOptions.execute(BuildProductOptions(), state, state.cache_dict[config_key_name], state.cache_dict[price_key_name], packageID, self.required)
            except Exception,e:
                print ("Failed with error:")
                print (str(e))
                print ("")

class BuildProductOptions:
    def __init__(self, required=False):
        self.required = required
    def execute(self, state, config_cache, price_cache, packageID, required):
        pkg_cfg_price_key = 'sl-pkg-'+str(packageID)+'-config-price-combined'
        pkg_cfg_price_key = {}
        priceFormat = '%s, {0:20} %s, %s, %s, %s'
        #"Location: {0:20} Revision {1}"
        self.required = required
        if 'selected-location' in state.cache_dict:
            selected_location = state.cache_dict['selected-location']
            selected_location_group_memberships_key = 'sl-location-'+str(selected_location)+'-memberships'
            selected_location_group_memberships_list_key = 'sl-location-'+str(selected_location)+'-membership-id-list'
            selected_location_groups = state.cache_dict[selected_location_group_memberships_key]
            if debug_printing:
                print ("") ;print ("")
                print ("selected_location_groups: ")
                print ("")
                state.pp.pprint(selected_location_groups)
        def output_when_location_specified(price, configuration):
            #if a datacenter is selcted, we can further restrict the list of items presented
            #currently we restrict the list to everything in a group the dc is part of, plus all the items that are
            #not part of a group. Possibly this is wrong, and will need to be further tightened to
            #remove duplicate/invalid items (items with no group id, where one exists witha group id for this dc)
            if price['locationGroupId'] == '' or price['locationGroupId'] in state.cache_dict[selected_location_group_memberships_list_key]:
                #if no datacenter is selected we return everything to the user, and let them figure it out.
                #print priceFormat %
                print '{: <6}'.format(price['id']), \
                    '{: <42}'.format(configuration['itemCategory']['name']), \
                    '{: <3}'.format(configuration['itemCategory']['id']), \
                    '{: <63}'.format(price['item']['description']), \
                    '{: <5}'.format(price['locationGroupId'])
                #(configuration['itemCategory']['name'], price['id'], configuration['itemCategory']['id'], price['item']['description'], price['locationGroupId'])
        def output_when_location_not_specified(price, configuration):
            print priceFormat % (price['locationGroupId'], configuration['itemCategory']['name'], configuration['itemCategory']['id'], price['id'], price['item']['description'])
        for configuration in config_cache:
            #iterate configurations
            if self.required:
                if (not configuration['isRequired']):
                    continue
            for price in price_cache:
                if ('categories' not in price):
                    continue
                if any((category.get('id') == configuration['itemCategory']['id']
                        for category in price['categories'])):
                    if 'selected-location' in state.cache_dict:
                        output_when_location_specified(price, configuration)
                    else:
                        output_when_location_not_specified(price,configuration)

class GetDataCenterLocations:
    def __init__(self, clioutput=False):
        self.clioutput = clioutput
    def execute(self, state):
        if 'sl-dc-locations' in state.cache_dict:
            print ("Found data in local cache, using that")
            print ("")
            if self.clioutput:
                state.pp.pprint(state.cache_dict['sl-dc-locations'])
                print ("")
        else:
            print ("Nothing found in local cache...")
            print ("Connecting to SoftLayer...")
            print ("")
            try:
                result = funcs_sl.get_datacenter_locations(state.slclient)
                if self.clioutput:
                    state.pp.pprint(result)
                state.overwrite_cache_dict_key("sl-dc-locations", result)
                print ("")
            except Exception,e:
                print ("Failed with error:")
                print (str(e))
                print ("")

class GetLocationGroups:
    def __init__(self, clioutput=False):
        self.clioutput = clioutput
    def execute(self, state):
        if 'sl-location-groups' in state.cache_dict:
            print ("Found data in local cache, using that")
            print ("")
            if self.clioutput:
                state.pp.pprint(state.cache_dict['sl-location-groups'])
                print ("")
        else:
            print ("Nothing found in local cache...")
            print ("Connecting to SoftLayer...")
            print ("")
            try:
                result = funcs_sl.get_location_groups(state.slclient)
                if self.clioutput:
                    state.pp.pprint(result)
                state.overwrite_cache_dict_key("sl-location-groups", result)
                print ("")
            except Exception,e:
                print ("Failed with error:")
                print (str(e))
                print ("")

class GetLocationGroupMembers:
    def __init__(self, clioutput=False):
        self.clioutput = clioutput
    def execute(self, state):
        print ("Enter the SoftLayer_Location_Group id:")
        choice = raw_input("> ")
        print ("You chose \"{0}\"").format(choice)
        locationGroupID = int(choice)
        location_group_key_name = 'sl-location-group-'+str(locationGroupID)+'-members'
        if  location_group_key_name in state.cache_dict:
            print ("Found data in local cache, using that")
            print ("")
            if self.clioutput:
                state.pp.pprint(state.cache_dict[location_group_key_name])
                print ("")
        else:
            print ("Nothing found in local cache...")
            print ("Connecting to SoftLayer...")
            print ("")
            try:
                result = funcs_sl.get_location_group_members(state.slclient, locationGroupID)
                if self.clioutput:
                    state.pp.pprint(result)
                state.overwrite_cache_dict_key(location_group_key_name, result)
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
    def __init__(self, clioutput=False):
        self.clioutput = clioutput
    def execute(self, state, location=0):
        if self.clioutput:
            print ("Enter the SoftLayer_Location id:")
            choice = raw_input("> ")
            print ("You chose \"{0}\"").format(choice)
        else:
            if debug_printing: print ("In GetIsMemberOfLocationGroups copy of location: "+str(location))
            choice = location
        locationID = int(choice)
        location_id_key_name1 = 'sl-location-'+str(locationID)+'-memberships'
        location_id_key_name2 = 'sl-location-'+str(locationID)+'-membership-id-list'
        if  location_id_key_name1 in state.cache_dict:
            if self.clioutput:
                print ("Found data in local cache, using that")
                print ("")
                state.pp.pprint(state.cache_dict[location_id_key_name1])
                print ("")
        else:
            if self.clioutput:
                print ("Nothing found in local cache...")
                print ("Connecting to SoftLayer...")
                print ("")
            try:
                result = funcs_sl.get_is_member_of_location_groups(state.slclient, locationID)
                if self.clioutput:
                    state.pp.pprint(result)
                    print ("")
                state.overwrite_cache_dict_key(location_id_key_name1, result)
                sl_loc_mem_id_list = []
                if debug_printing:
                    print ("")
                    print ("In GetIsMemberOfLocationGroups, iterating location group id's for the selected dc:")
                for i in s.cache_dict[location_id_key_name1]:
                    if debug_printing: print i.get('id')
                    sl_loc_mem_id_list.append(i.get('id'))
                state.overwrite_cache_dict_key(location_id_key_name2, sl_loc_mem_id_list)
            except Exception,e:
                print ("Failed with error:")
                print (str(e))
                print ("")

class InteractiveExec:
    def execute(self, state):
        print ("")
        print ("Think about it: You supplied production SL credentials")
        print ("and now you chose the option titled 'Break stuff'.")
        print ("Press <enter> QUICKLY and we'll forget this happened.")
        print ("")
        choice = raw_input("> ")
        print ("You typed \"{0}\"").format(choice)
        exec(choice)

class SpecifyDatacenter:
    def execute(self, state):
        if not 'sl-dc-locations' in state.cache_dict:
            print "Local cache doesn't contain datacenter data, fixing that..."
            GetDataCenterLocations(False).execute(state)
        print ("List of valid datacenter's currently cached:")
        state.pp.pprint(state.cache_dict['sl-dc-locations'])
        print ("Specify datacenter id:")
        choice = raw_input("> ")
        print ("You chose \"{0}\"").format(choice)
        state.cache_dict['selected-location'] = int(choice)
        PopulateSelectedLocationGroupMembership.execute(PopulateSelectedLocationGroupMembership(), state=state, location=int(choice))

class PopulateSelectedLocationGroupMembership:
    def execute(self, state, location):
        self.location = location
        if debug_printing: print "In PopulateSelectedLocationGroupMembership"
        if debug_printing: print "Local copy of location: "+str(self.location)
        GetIsMemberOfLocationGroups(clioutput=False).execute(state, location=self.location)

class ShowDatacenter:
    def execute(self, state):
        print ("Currently selected datacenter is:")
        print state.cache_dict['selected-location']

class ShowWipDict:
    def execute(self, state):
        print ("WIP dict for in progress quote looks like:")
        state.pp.pprint(state.wip_dict)

menu_main = Location("menu_main",
    "Press the number then <enter> for the option you want:",
    [Option("Download Quote Pdf for a specific quote", DownloadQuotePdf()),
    Option("(MENU) Manage Quotes", GoToLocation("menu_manage_quotes")),
    Option("Specify datacenter", SpecifyDatacenter()),
    Option("Re-verify existing quote on control portal", ReverifyExistingQuote()),
    Option("Duplicate existing quote on control portal", DuplicateExistingQuote()),
    Option("<SL Not Imlemented> Create quote cart", Message("According to https://control.softlayer.com/support/tickets/23363617 (one of Ewan's accounts) regarding functionality: ['SoftLayer_Billing_Order_Cart'].createCart(container) 'the customer won't be able to create a cart, because this is a feature which is on hold'")),
    Option("Show all quotes in account", ShowAllQuotes()),
    Option("Show all active SoftLayer_product_Package(s)", ShowAllProductPackages(active=True, clioutput=True)),
    Option("List SoftLayer_Product_Package *required* options for a given package", ListPackageOptions(required=True)),
    Option("List SoftLayer_Product_Package *all* options for a given package", ListPackageOptions(required=False)),
    Option("List Location_DataCenter (DC locations)", GetDataCenterLocations(clioutput=True)),
    Option("List Location_Group(s)", GetLocationGroups(clioutput=True)),
    Option("List Location_Group members", GetLocationGroupMembers(clioutput=True)),
    Option("List type of a Location_Group",  GetLocationGroupType()),
    Option("List Location_Group(s) location is a member of", GetIsMemberOfLocationGroups(clioutput=True)),
    Option("Break stuff", InteractiveExec()),
    Option("Exit to shell", CloseDown("Goodbye."))])

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
