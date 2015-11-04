#!/usr/bin/python
import SoftLayer
#increase default timeout to reduce false failure
#on slow or conjested connections
client = SoftLayer.create_client_from_env(timeout=240)

#client = SoftLayer.Client(username=myuser, api_key=mykey, endpoint_url=SoftLayer.API_PUBLIC_ENDPOINT)


cache_dict = {}

import SoftLayer
client = SoftLayer.create_client_from_env(timeout=240)
packageID = 46
required = True
categoryObjectMask = "mask[isRequired, itemCategory[id, name]]"
configurations = client['Product_Package'].getConfiguration(id=packageID, mask=categoryObjectMask)
pricesObjectMask = "mask[id;item.description;categories.id,locationGroupId]"
prices = client['Product_Package'].getItemPrices(id=packageID, mask=pricesObjectMask)

config_key_name = 'sl-pkg-'+str(packageID)+'-configs'
price_key_name = 'sl-pkg-'+str(packageID)+'-prices'

cache_dict[config_key_name] = {}
cache_dict[price_key_name] = {}

cache_dict[config_key_name] = configurations
cache_dict[price_key_name] = prices

cache_dict.keys()

priceFormat = '%s, %s, %s, %s, %s'
for configuration in cache_dict[config_key_name]:
    if required:
        if (not configuration['isRequired']):
            continue
    for price in cache_dict[price_key_name]:
        if ('categories' not in price):
            continue
        if any((category.get('id') == configuration['itemCategory']['id']
                for category in price['categories'])):
            print priceFormat % (configuration['itemCategory']['name'], configuration['itemCategory']['id'], price['locationGroupId'], price['id'], price['item']['description'])







import pprint

#https://forums.softlayer.com/forum/softlayer-developer-network/general-discussion/80475-provision-bare-metal-instance-via-rest-api
#We have a "generic" order container, which is the SoftLayer_Container_Product_Order;
#by specifying the correct package ID and prices on it, it can be used to place orders for CCIs (virtual guests),
#Bare Metals and/or regular dedicated servers (even mixed on the same order!).

#http://sldn.softlayer.com/reference/services/SoftLayer_Product_Order/placeOrder

#define a valid order "container?"
order = {
'orderContainers': [
    {
    'complexType': 'SoftLayer_Container_Product_Order_Hardware_Server',
    'quantity': 1,
    'hardware': [
          {
            'hostname': 'test1',
            'domain': 'example.com',
          }
    ],
    'containerIdentifier': 'myContainer',
    'location': '449596',
    'packageId': 248, # Intel Xeon 3200 Series
    'prices': [
                {'id': 46534},
                {'id': 49445},
                {'id': 876}, # Disk Controller - Non-RAID
                {'id': 49859}, # First Hard Drive - 73GB SA-SCSI 10K RPM
                {'id': 53507}, #bandwidth
                {'id': 20963}, #os
                {'id': 272}, # Uplink Port Speeds - 10 Mbps Public & Private Networks
                {'id': 906}, # Remote Management - Reboot / KVM over IP
                {'id': 21}, # Primary IP Addresses - 1 IP Address
                {'id': 55}, # Monitoring - Host Ping
                {'id': 57}, # Notification - Email and Ticket
                {'id': 60}, # Response - 24x7x365 NOC Monitoring, Notification, and Response
                {'id': 420}, # VPN Management - Private Network - Unlimited SSL VPN Users & 1 PPTP VPN User per account
                {'id': 418}, # Vulnerability Assessments & Management - Nessus Vulnerability Assessment & Reporting
    ],
    },
    {
    'complexType': 'SoftLayer_Container_Product_Order_Virtual_Guest',
    'quantity': 1,
    'virtualGuests': [
          {
            'hostname': 'test2',
            'domain': 'example.com',
          }
    ],
    'containerIdentifier': 'myoTHERContainer',
    'location': '449596',
    'packageId': 46,
    'useHourlyPricing': False,
    'prices': [
               {'id': 1640},  # 1 x 2.0 GHz Core
               {'id': 1644},  # 1 GB RAM
               {'id':  905},  # Reboot / Remote Console
               {'id':  272},  # 10 Mbps Public & Private Networks
               {'id':  1800},  # 1000 GB Bandwidth
               {'id':   21},  # 1 IP Address
               {'id': 2202},  # 25 GB (SAN)
               {'id': 1684},  # CentOS 5 - Minimal Install (32 bit)
               {'id':   55},  # Host Ping Monitoring
               {'id':   57},  # Email and Ticket Notifications
               {'id':   58},  # Automated Notification Response
               {'id':  420},  # Unlimited SSL VPN Users & 1 PPTP VPN User per account
               {'id':  418}
    ],
    },
],
}

from pprint import pprint as pp
pp = pprint.PrettyPrinter(indent=4)


    #this can be used to enumberate all orders in the account
#pp.pprint(client['Billing_Order'].getAllObjects())

#quoteId = '6067535'
# So we can talk to the SoftLayer API:
import SoftLayer.API

orderQuoteId = '1558395'

def getOrderContainer(quote_id):
    container = client['Billing_Order_Quote'].getRecalculatedOrderContainer( \
        id=quote_id)
    return container #container['orderContainers'][0]

    #invoke the function above:
container = getOrderContainer(orderQuoteId)
    #output that stuff:
pp.pprint(container)

    #https://softlayer.github.io/python/order_quote/


    #this appears to work, but hasn't yet been useful
quoteKey = '8b3a868b22e56543e066cd97af8d72c9'
#quote = client['Billing_Order_Quote'].getQuoteByQuoteKey(quoteKey)

#quoteObj = client['Billing_Order_Quote'].getObject(id=1558305)



import SoftLayer
client = SoftLayer.create_client_from_env(timeout=240)
print client['Account'].getQuotes()

class download_quote_pdf:
    def __init__(self, msg):
        self.msg = msg
    def execute(self, state):
        print self.msg


action_download_quote_pdf(client, menu_download_quote_pdf())


def menu_download_quote_pdf():
    print ("")
    print ("")
    print ("Enter the id for the quote you wish to download:")
    user_input = raw_input("id: ")
    return int(user_input)

def download_quote_pdf(client, quoteID):
    #because: logic!? Anyway... this works
    return client['Billing_Order_Quote'].getPdf(id=quoteID)


def pdfPickle(output_file_name_base, binary_obj):
    import pickle
    pickleFileName = "./SL-Quote-ID"+str(output_file_name_base)+".pdf"
    pickleFile = open(pickleFileName, 'wb')
    pickle.dump(binary_obj, pickleFile, pickle.HIGHEST_PROTOCOL)
    pickleFile.close()

def legacy():

    quoteID = funcs_cli_menu.download_quote_pdf()
    print ("Connecting to SoftLayer...")
    quotePDF = funcs_sl.download_quote_pdf(client, quoteID)
    print ("Writing output file ")
    funcs_fs.pdfPickle(quoteID, quotePDF)
