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

class prices_container:
    container_count = (0)
    def __init__(self, prices_list):
        prices_container.container_count += 1
        self.container = prices_list
    def displayCount(self):
        print "Total Containers %d" % order_container.container_count
    def displayContainer(self):
        print "self: ", self.container#,  ", Quantity: ", self.quantity
    def deleteItem(self, item):
        #self.container.remove({'id': 906})
        self.container.remove(item)
    def addItem(self, item):
        self.container.append(item)
    def returnSelf(self):
        return self.container


price_container = prices_container(my_prices)
'''
price_container.displayContainer()
price_container.deleteItem({'id': 906})
print
price_container.displayContainer()
print
price_container.addItem({'id': 906})
price_container.displayContainer()
'''

my_hw = {}
my_hw['hostname'] = 'test1'
my_hw['domain'] = 'example.com'

class hardware_container:
    container_count = (0)
    def __init__(self, hardware_dict):
        hardware_container.container_count += 1
        self.container = hardware_dict
    def displayCount(self):
        print "Total Containers %d" % hardware_container.container_count
    def displayContainer(self):
        print "self: ", self.container#,  ", Quantity: ", self.quantity
    def deleteItem(self, key):
        del self.container[key]
    def addItem(self, item):
        #print addition
        self.container = dict(self.container, **item)
    def returnSelf(self):
        return self.container


hw_container = hardware_container(my_hw)
'''
hw_container.displayContainer()
print
hw_container.deleteItem('hostname')
hw_container.displayContainer()
my_oo = {}
my_oo['hostname'] = 'test1'
hw_container.addItem(my_oo)
print
hw_container.displayContainer()
hw_container.displayCount()
'''

my_oc = {}
my_oc['complexType'] = 'SoftLayer_Container_Product_Order_Hardware_Server'
my_oc['quantity'] = 1
my_oc['hardware'] = [hw_container.returnSelf()]
#my_oc['containerIdentifier'] = 'myContainer'
my_oc['packageId'] = '248'
my_oc['prices'] = price_container.returnSelf()
    #prices doesn't need [] because of datatype?
my_oc['location'] = '449596'


class product_container:
    container_count = (0)
    def __init__(self, order_dict):
        product_container.container_count += 1
        self.container = order_dict
    def displayCount(self):
        print "Total Containers %d" % product_container.container_count
    def displayContainer(self):
        print "self: ", self.container#,  ", Quantity: ", self.quantity
    def deleteItem(self, key):
        del self.container[key]
    def addItem(self, item):
        self.container = dict(self.container, **item)
    def returnSelf(self):
        return self.container


product1 = product_container(my_oc)
'''
product1.displayContainer()
print
product1.deleteItem('complexType')
product1.displayContainer()
my_oo = {}
my_oo['complexType'] = 'SoftLayer_Container_Product_Order_Hardware_Server'
product1.addItem(my_oo)
'''
print
#product1.displayContainer()
#print product1.returnSelf()
#product1.displayCount()

my_order = {}
my_order['orderContainers'] = [product1.returnSelf()]

class order_container:
    container_count = (0)
    def __init__(self, order_dict):
        order_container.container_count += 1
        self.container = order_dict
    def displayCount(self):
        print "Total Containers %d" % order_container.container_count
    def displayContainer(self):
        print "self: ", self.container#,  ", Quantity: ", self.quantity
    def deleteItem(self, key):
        del self.container[key]
    def addItem(self, item):
        self.container = dict(self.container, **item)
    def returnSelf(self):
        return self.container

order = order_container(my_order)

import pprint
from pprint import pprint as pp
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(order.returnSelf())

import SoftLayer
#increase default timeout to reduce false failure
#on slow or conjested connections
client = SoftLayer.create_client_from_env(timeout=240)
client['Product_Order'].verifyOrder(order.returnSelf());
client['Product_Order'].placeQuote(order.returnSelf());

'''
import gc
for obj in gc.get_objects():
    if isinstance(obj, order_container):
        print obj.containerID, obj.packageID
'''
