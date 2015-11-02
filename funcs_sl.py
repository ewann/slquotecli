import SoftLayer
    #needed to interact with SL api

def conn_obj():
    client = SoftLayer.create_client_from_env(timeout=240)
    return client

def list_all_quotes(client):
    return client['Account'].getQuotes()

def download_quote_pdf(client, quoteID):
    #because: logic!? Anyway... this works
    return client['Billing_Order_Quote'].getPdf(id=quoteID)

def list_all_product_packages(client):
    object_mask = "mask[id, name]"
    return client['Account'].getActivePackages(mask=object_mask)
        #This approach came from http://sldn.softlayer.com/blog/sthompson/virtual-guest-ordering
    #return client['Product_Package'].getAllObjects(mask=object_mask)

def get_existing_quote_container(client, quoteID):
    container = client['Billing_Order_Quote'].getRecalculatedOrderContainer( \
        id=quoteID)
    return container #['orderContainers'][0]

def verify_quote_or_order(client, container):
    return client['Product_Order'].verifyOrder(container)

def place_quote(client, container):
    return client['Product_Order'].placeQuote(container)
    #same approach can be used wih an existing quote id, as well as a quote container?
#result = client['Billing_Order_Quote'].verifyOrder(orderQuoteId)

def create_order_cart(client, container):
    return client['Product_Order_Cart'].createCart(container)

def list_product_package_options(client, package, required):
    #package = 248 #46 for virtual server, see sl-list-pkgs.py for more

    #client = SoftLayer.Client(username=apiUsername, api_key=apiKey)
    categoryObjectMask = "mask[isRequired, itemCategory[id, name]]"

    configurations = client['Product_Package'].getConfiguration(
        id=package, mask=categoryObjectMask)

    pricesObjectMask = "mask[id;item.description;categories.id,locationGroupId]"

    prices = client['Product_Package'].getItemPrices(
        id=package, mask=pricesObjectMask)

    headerFormat = '%s - %s:'
    priceFormat = '    %s -- %s'
    for configuration in configurations:
        if required:
            if (not configuration['isRequired']):
                continue
        print headerFormat % (configuration['itemCategory']['name'],
                              configuration['itemCategory']['id'])
        for price in prices:
            if ('categories' not in price):
                continue
            if any((category.get('id') == configuration['itemCategory']['id']
                    for category in price['categories'])):
                print "LocGrpID: ", price['locationGroupId'], priceFormat % (price['id'], price['item']['description'])
                    #locationGroupId is the reason some items appear multiple times - allows us to restrict the list if the dc is known

def get_datacenter_locations(client):
    object_mask = "mask[id, longName, name]"
    return client['Location_Datacenter'].getDatacenters(mask=object_mask)

def get_location_groups(client):
    object_mask = "mask[id,description]"
    return client['Location_Group'].getAllObjects(mask=object_mask)

def get_location_group_members(client,groupID):
    # querying location groups - needed to identify pricing items
    object_mask = "mask[id,description]"
    return client['Location_Group'].getLocations(id=groupID)

def get_location_group_type(client,groupID):
    return client['Location_Group'].getLocationGroupType(id=groupID)

def get_is_member_of_location_groups(client,locationID):
    return client['Location'].getGroups(id=locationID)

    #this can be used to enumberate all orders in the account
#pp.pprint(client['Billing_Order'].getAllObjects())
