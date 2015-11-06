#!/usr/bin/python
#menu code based on the example at:
#http://codereview.stackexchange.com/questions/65305/making-user-menus-in-a-text-based-game

class State:
    def __init__(self, starting_loc):
        self.alive = True
        self.location = starting_loc
        self.locations = {}
        #state for slquotecli goes here?
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
        #missing logic appears to be:
                            #client['Product_Package'].getLocations(id=xyz)
        #if a target datacenter is configured:
            #for each package:
                #if output of getLocations is already cached:
                    #if current dc is in scope, print package id
                #else:
                    #cache the output of #client['Product_Package'].getLocations(id=xyz)
                    ##if current dc is in scope, print package id
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
            #currently we restrict the list to everything in a group the dc is part of,
            #we are currently filtering out:
            # all the items that are not part of a group.
            #Possibly this is wrong, but it appears correct based on attempts to order items with location group id's
            if price['locationGroupId'] == '': #or price['locationGroupId'] in state.cache_dict[selected_location_group_memberships_list_key]:
                #if no datacenter is selected we return everything to the user, and let them figure it out.
                #print priceFormat %
                print '{: <6}'.format(price['id']), \
                    '{: <42}'.format(configuration['itemCategory']['name']), \
                    '{: <3}'.format(configuration['itemCategory']['id']), \
                    '{: <5}'.format(price['locationGroupId']), \
                    '{: <63}'.format(price['item']['description'])
        def output_when_location_not_specified(price, configuration):
            print '{: <6}'.format(price['id']), \
                '{: <42}'.format(configuration['itemCategory']['name']), \
                '{: <3}'.format(configuration['itemCategory']['id']), \
                '{: <5}'.format(price['locationGroupId']), \
                '{: <63}'.format(price['item']['description'])
            #print priceFormat % (price['locationGroupId'], configuration['itemCategory']['name'], configuration['itemCategory']['id'], price['id'], price['item']['description'])
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

class ShowInprogressQuote:
    def execute(self, state):
        print ("The currently selected & in progress quote container looks like:")
        #state.pp.pprint(state.cache_dict['currently_selected_product_container'])

        quote = {}
        quoteContainers = []
        containers = ListLoadedProductContainers(clioutput=False).execute(state)
        for item in containers:
            state.cache_dict.get(item)
            quoteContainers.append(state.cache_dict.get(item))
        quote['orderContainers'] = quoteContainers
        quote
        state.pp.pprint(quote)

class CreateProductContainer:
    def execute(self, state):
        print ("")
        print ("Quotes (and fwiw orders) are composed of one or more containers")
        print ("If you need multiple servers of the same configuration")
        print ("it makes sense to use the quantity attribute of the container")
        print ("as opposed to creating one container per server")
        print ("unless you have no other task to complete right now...")
        print ("")
        print ("Enter a name (using chars: [A-z1-0]) for this container")
        print ("")
        print ("If you specify the name of an existing container, we'll overwrite it.")
        print ("You won't get warned again before that happens.")
        print ("")
        print ("Your container will be prefixed: container-<your_container_name>")
        print ("Eg: You enter: test")
        print ("The container created will be called: container-test")
        print ("")
        choice = raw_input("> ")
        print ("You typed \"{0}\"").format(choice)
        if choice == '':
            print ("Noting entered, aborted")
        else:
            container_name = "container-"+(str(choice))
            state.overwrite_cache_dict_key(container_name, {})
            state.cache_dict[container_name]['complexType'] = 'SoftLayer_Container_Product_Order_Hardware_Server'
            state.cache_dict[container_name]['quantity'] = 1
            state.cache_dict[container_name]['hardware'] = []
            state.cache_dict[container_name]['containerIdentifier'] = container_name
            state.cache_dict[container_name]['location'] = 3
            state.cache_dict[container_name]['prices'] = []

class ListLoadedProductContainers:
    def __init__(self, clioutput=False):
        self.clioutput = clioutput
    def execute(self, state):
        if self.clioutput:
            print ("")
            print ("The following package containers are currently cached / loaded:")
            print ("")
        #result = {k:v for (k,v) in state.cache_dict.iteritems() if 'container-' in k}
            #syntax not supported in python pre 2.7.x, so instead using:
        result = {}
        for k,v in state.cache_dict.iteritems():
            if 'container-' in k:
                result[k] = v
        if self.clioutput:
            print result.keys()
            print ("")
            print ("")
        return result.keys()

class UnloadProductContainer:
    def execute(self, state):
        print ("")
        print ("Enter the container name you wish to unload")
        print ("(this doesn't currently save) the container anywhere")
        print ("")
        choice = raw_input("> ")
        print ("You typed \"{0}\"").format(choice)
        if choice == '' or not "container-" in choice:
            print ("Invalid request, aborted")
        else:
            if choice in state.cache_dict: del state.cache_dict[choice]

class SelectProductContainerForEditing:
    def execute(self, state):
        print ("")
        print ("Enter the container name you wish to edit:")
        print ("")
        choice = raw_input("> ")
        print ("You typed \"{0}\"").format(choice)
        #result = {k:v for (k,v) in state.cache_dict.iteritems() if choice in k}
            #syntax not supported in python pre 2.7.x, so instead using:
        result = {}
        for k,v in state.cache_dict.iteritems():
            if choice in k:
                result[k] = v
        if not bool(result):
            print ("")
            print ("Something went wrong, we couldn't find that product container")
            print ("Maybe you didn't create it yet?")
            print ("")
        else:
            if debug_printing:
                print ("")
                print ("In: SelectProductContainerForEditing, else... (we found the container in cache_dict)")
                print ("result of container lookup: ")
                print(result)
                print ("")
                print ("In: SelectProductContainerForEditing, printing state.cache_dict.keys()")
                print(state.cache_dict.keys())
            state.cache_dict['currently_selected_product_container'] = choice

class ShowCurrentlySelectedProductContainer:
    def execute(self, state):
        if 'currently_selected_product_container' in state.cache_dict:
            print ("")
            print ("The currently selected product container is:")
            print ("")
            print state.cache_dict['currently_selected_product_container']
            print ("")
            print ("")
        else:
            print ("no product containers are currently selected")
            if debug_printing: print ("cache dict looks like: "+ str(state.cache_dict.keys()))

class VerifyPlaceQuote:
    def __init__(self, placeQuote=False):
        self.placeQuote = placeQuote
    def execute(self, state):
        quote = {}
        quoteContainers = []
        containers = ListLoadedProductContainers(clioutput=False).execute(state)
        for item in containers:
            state.cache_dict.get(item)
            quoteContainers.append(state.cache_dict.get(item))
        quote['orderContainers'] = quoteContainers
        quote
        state.pp.pprint(quote)
        print ("Connecting to SoftLayer...")
        print ("")
        try:
            if self.placeQuote:
                funcs_sl.place_quote(state.slclient, quote)
                print ("")
                print ("Quote SUCCESSFULLY PLACED - you can safely place a quote using these package containers")
            else:
                state.pp.pprint(funcs_sl.verify_quote_or_order(state.slclient, quote))
                print ("")
                print ("Quote SUCCESSFULLY VERIFIED - you can safely place a quote using these package containers")
        except Exception,e:
            print ("Failed with error:")
            print (str(e))
            print ("")

class ChangeDeploymentLocation:
    def execute(self, state):
        print ("")
        print ("Enter the datacenter id you would like to specify for the selected container:")
        print ("")
        choice = raw_input("> ")
        print ("You typed \"{0}\"").format(choice)
        #missing a check that something valid comes back from:
        #result = state.cache_dict['currently_selected_product_container']
        if not state.cache_dict.has_key('currently_selected_product_container'):
            print ("No product container has been selected yet...")
            SelectProductContainerForEditing().execute(state)
        container = state.cache_dict['currently_selected_product_container']
        state.cache_dict[container]['location'] = int(choice)

class ChangePackageId:
    def execute(self, state):
        print ("")
        print ("Enter the package id you would like to specify for the selected container:")
        print ("")
        choice = raw_input("> ")
        print ("You typed \"{0}\"").format(choice)
        if not state.cache_dict.has_key('currently_selected_product_container'):
            print ("No product container has been selected yet...")
            SelectProductContainerForEditing().execute(state)
        container = state.cache_dict['currently_selected_product_container']
        state.cache_dict[container]['packageId'] = int(choice)

class SpecifyPriceIds:
    def execute(self, state):
        print ("")
        print ("Enter the list of price id's you would like to specify for the selected container:")
        print ("These need to be comma separated")
        print ("")
        print ("At the time of writing, (5th November 2015) the following is a valid set of")
        print ("prices for package id 248 in datacenter 449596")
        print ("46534,49445,876,49859,53507,20963,272,906,21,55,57,60,420,418")
        print ("")
        choice = raw_input("> ")
        print ("You typed \"{0}\"").format(choice)
        if not state.cache_dict.has_key('currently_selected_product_container'):
            print ("No product container has been selected yet...")
            SelectProductContainerForEditing().execute(state)
        container = state.cache_dict['currently_selected_product_container']
        prices = choice.split(",")
        output_prices = []
        for price in prices:
            temp_dict = {}
            temp_dict['id'] = price
            output_prices.append(temp_dict)
        state.cache_dict[container]['prices'] = output_prices

class ExportProductContainersToJson:
    def execute(self, state):
        for k,v in state.cache_dict.iteritems():
            if 'container-' in k:
                try:
                    if debug_printing:
                        print ("writing object: "+str(k))
                        state.pp.pprint(v)
                    funcs_fs.jsonGateway("save", "./"+k+".json", v)
                except Exception,e:
                    print ("Failed with error:")
                    print (str(e))
                    print ("")

class ImportProductContainersFromJson:
    def execute(self, state):
        try:
            containerFiles = funcs_fs.enumFilesInDir(".",".json")
            for file in containerFiles:
                if debug_printing:
                    print ("Filename: "+str(file))
                    state.pp.pprint(funcs_fs.jsonGateway("load", "./"+file))
                if file.endswith('.json'): container_name = file[:-5]
                sans_unicode = funcs_fs.byteify(funcs_fs.jsonGateway("load", "./"+file))
                if debug_printing: state.pp.pprint(sans_unicode)
                state.cache_dict[container_name] = sans_unicode
        except Exception,e:
            print ("Failed with error:")
            print (str(e))
            print ("")


menu_main = Location("menu_main",
            #FEATURE REQUEST: catch ctrl-c / other keyboard escapes?
    "Press the number then <enter> for the option you want:",
    [Option("Specify target datacenter id", SpecifyDatacenter()),
    Option("Show all SoftLayer_product_Package(s) active in this account", ShowAllProductPackages(active=True, clioutput=True)),
            #BUG - api is not being checked to confirm packages are available in the selected datacenter
                #WORKAROUND: validate a quote with only the location & package set to confirm item is orderable
    Option("List SoftLayer_Product_Package *required* options for a given package (use 'id' from menu option 2)", ListPackageOptions(required=True)),
    Option("List SoftLayer_Product_Package *all* options for a given package (use 'id' from menu option 2)", ListPackageOptions(required=False)),
            #BUG: container type is hardcoded, meaning that virtual servers (cci's), gateways etc cannot be quoted
                #NO-WORKAROUND
            #BUG: quantity is hardcoded to 1 per containers
                #WORKAROUND: create a container per server required
    Option("Create product container", MultiAction([ListLoadedProductContainers(clioutput=True),
                                            CreateProductContainer(),
                                            ListLoadedProductContainers(clioutput=True),
                                            SelectProductContainerForEditing()])),
            #FIXED? 20151106 #BUG? seems to be a dependency on next item that doesn't get auto resolved
    Option("Select a product container for editing", MultiAction([ListLoadedProductContainers(clioutput=True),
                                                                ShowCurrentlySelectedProductContainer(),
                                                                SelectProductContainerForEditing(),
                                                                ShowCurrentlySelectedProductContainer(),
                                                                GoToLocation("menu_main")])),
    Option("List existing product container(s)", ListLoadedProductContainers(clioutput=True)),
    Option("Unload product container(s) - make sure you save them first", MultiAction([ListLoadedProductContainers(clioutput=True),
                                            UnloadProductContainer()])),
    Option("Set container deployment location (use id from menu option 0 / 15)", MultiAction([ShowCurrentlySelectedProductContainer(),
                                                                ShowInprogressQuote(),
                                                                ChangeDeploymentLocation(),
            #FIXED? 20151106 #SEEMS TO BE A BUG - needs triage - resolution appears to come from (MENU) Select a product.... above
                                                                ShowInprogressQuote(),
                                                                GoToLocation("menu_main")])),
    Option("Set container package id (use id from menu option 1)", MultiAction([ShowCurrentlySelectedProductContainer(),
                                                                ShowInprogressQuote(),
                                                                ChangePackageId(),
                                                                ShowInprogressQuote(),
                                                                GoToLocation("menu_main")])),
            #FEATURE requirement: display friendly text as well as price ID's
    Option("Set container price ids (use column 1 from menu option 2 / 3)", MultiAction([ShowCurrentlySelectedProductContainer(),
                                                                ShowInprogressQuote(),
                                                                SpecifyPriceIds(),
                                                                ShowInprogressQuote(),
                                                                GoToLocation("menu_main")])),
            #FEATURE Requirement: output id's as comma separated list in case of need to chance
    Option("Show the in progress quote containers", ShowInprogressQuote()),
    Option("Verify a quote (uses all loaded product containers)", VerifyPlaceQuote()),
    Option("Place a quote (uses all loaded product containers)", VerifyPlaceQuote(placeQuote=True)),
    Option("Export Product containers to disk (JSON)", ExportProductContainersToJson()),
    Option("Import Product containers (*.json) in current dir", ImportProductContainersFromJson()),
    Option("Download Quote Pdf for an existing portal quote id", DownloadQuotePdf()),
    Option("List Location_DataCenter (DC locations)", GetDataCenterLocations(clioutput=True)),
    Option("Show currently selected datacenter", ShowDatacenter()),
    Option("Troubleshooting options menu", GoToLocation("menu_troubleshooting")),
    Option("Exit to shell", CloseDown("Goodbye."))])

menu_troubleshooting = Location("menu_troubleshooting",
    "Press the number then <enter> for the option you want:",
    [Option("(MENU) Return to previous menu", GoToLocation("menu_main")),
    Option("Break stuff", InteractiveExec()),
    Option("Re-verify existing quote on control portal", ReverifyExistingQuote()),
    Option("Duplicate existing quote on control portal", DuplicateExistingQuote()),
    Option("List Location_Group(s)", GetLocationGroups(clioutput=True)),
    Option("List Location_Group members", GetLocationGroupMembers(clioutput=True)),
    Option("List type of a Location_Group",  GetLocationGroupType()),
    Option("List Location_Group(s) location is a member of", GetIsMemberOfLocationGroups(clioutput=True)),
    Option("Show all quotes in account", ShowAllQuotes()),
    Option("List existing order container(s)", Message("Not implemented")),
    Option("<SL Not Imlemented> Create quote cart", Message("According to https://control.softlayer.com/support/tickets/23363617 \
        (one of Ewan's accounts) regarding functionality: ['SoftLayer_Billing_Order_Cart'].createCart(container) \
        'the customer won't be able to create a cart, because this is a feature which is on hold'"))])

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
        import pprint
        import pickle #needed by funcs_fs.pdfPickle
        import json #needed by funcs_fs.jsonGateway
        import os #needed by funcs_fs.enumFilesInDir
        import funcs_sl #functions that interact with SL api
        import funcs_fs #functions that interact with local filesystem
        s = State(menu_main)
        s.addloc(menu_main)
        s.addloc(menu_troubleshooting)
        s.location.start()
        while(s.alive):
            s.location.print_opts()
            s.location.get_choice(s)
