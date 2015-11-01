#!/usr/bin/python
import SoftLayer
#increase default timeout to reduce false failure
#on slow or conjested connections
client = SoftLayer.create_client_from_env(timeout=240)
#
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
    #verify the order is placeable
#client['Product_Order'].verifyOrder(order);
    #lodge the order as a quote - ie: don't execute a financial transaction
    #but make it available for later placement:
#client['Product_Order'].placeQuote(order);
    #this next statement needs further review:
from pprint import pprint as pp
pp = pprint.PrettyPrinter(indent=4)

    #these next two lines haven't yielded anything useful yet
#thisquote = client['Billing_Order', '6067535']
#pp.pprint(thisquote)#client['Billing_Order_Quote'].getPdf(thisquote))

    #this can be used to enumberate all orders in the account
#pp.pprint(client['Billing_Order'].getAllObjects())

#quoteId = '6067535'
# So we can talk to the SoftLayer API:
import SoftLayer.API

orderQuoteId = '1558395'

def getOrderContainer(quote_id):
    container = client['Billing_Order_Quote'].getRecalculatedOrderContainer( \
        id=quote_id)
    return container['orderContainers'][0]

    #invoke the function above:
container = getOrderContainer(orderQuoteId)
    #output that stuff:
pp.pprint(container)

    #verifying the order for orderQuoteId should never fail
#result = client['Billing_Order_Quote'].verifyOrder(orderQuoteId)
    #next we verify the order using the order container we extracted
#result = client['Product_Order'].verifyOrder(container)
    #next we register a new quote using the verified container
#result = client['Product_Order'].placeQuote(container)
    #https://softlayer.github.io/python/order_quote/
#pp.pprint(result)

#quotes = client['Account'].getQuotes()
#pp.pprint(quotes)

    #this appears to work, but hasn't yet been useful
quoteKey = '8b3a868b22e56543e066cd97af8d72c9'
#quote = client['Billing_Order_Quote'].getQuoteByQuoteKey(quoteKey)

#quoteObj = client['Billing_Order_Quote'].getObject(id=1558305)

    #because: logic!? Anyway... this works
#result = client['Billing_Order_Quote'].getPdf(id=1558305)
#pp.pprint(result)


def pdfPickle(bin_obj):
    import pickle
    pickleFileName = "out.pdf"
    pickleFile = open(pickleFileName, 'wb')
    pickle.dump(bin_obj, pickleFile, pickle.HIGHEST_PROTOCOL)
    pickleFile.close()
