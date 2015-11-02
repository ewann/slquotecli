#http://www.bogotobogo.com/python/python_dictionaries_tuples.php

import pprint
from pprint import pprint as pp
pp = pprint.PrettyPrinter(indent=4)

my_prices = []
my_prices.append({'id': 46534})
my_prices.append({'id': 49445})
my_prices.append({'id': 876})
my_prices.append({'id': 49859})
my_prices.append({'id': 53507})
my_prices.append({'id': 20963})
my_prices.append({'id': 272})
my_prices.append({'id': 906})
my_prices.append({'id': 21})
my_prices.append({'id': 55})
my_prices.append({'id': 57})
my_prices.append({'id': 60})
my_prices.append({'id': 420})
my_prices.append({'id': 418})

my_hw = {}
my_hw['hostname'] = 'test1'
my_hw['domain'] = 'example.com'

my_oc = {}
my_oc['complexType'] = 'SoftLayer_Container_Product_Order_Hardware_Server'
my_oc['quantity'] = 1
my_oc['hardware'] = my_hw
my_oc['containerIdentifier'] = 'myContainer'
my_oc['packageId'] = '248'
my_oc['prices'] = my_prices
my_oc['location'] = '449596'

my_dict = {}
my_dict['orderContainers'] = [my_oc]

order = my_dict

import SoftLayer
#increase default timeout to reduce false failure
#on slow or conjested connections
client = SoftLayer.create_client_from_env(timeout=240)
client['Product_Order'].verifyOrder(order);

client['Product_Order'].placeQuote(order);

pp.pprint(order)


'''
L1 = ['a','b','c']
L2 = ['1','2','3','4','5']

res_list = [
    {'grade': 'ok', 'rc': 0},
    {'grade': 'warning', 'rc': 1}
]

sub_dict = {
    'count': 0,
    'results': res_list
}

my_dict = {}
for l1 in L1:
    my_dict[l1] = {}

for l1 in L1:
    for l2 in L2:
        my_dict[l1][l2] = sub_dict

print my_dict
