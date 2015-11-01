#!/usr/bin/python
#https://sldn.softlayer.com/blog/bpotter/Going-Further-SoftLayer-API-Python-Client-Part-3
#^^^ more good things in there
import SoftLayer
import os
#https://gist.github.com/underscorephil/4067364
#http://softlayer-python.readthedocs.org/en/latest/api/managers/vs.html
SL_API_USERNAME = os.environ.get("SL_API_USERNAME", None)
SL_API_KEY = os.environ.get("SL_API_KEY", None)


apiUsername = SL_API_USERNAME
apiKey = SL_API_KEY
package = 248 #46 for virtual server, see sl-list-pkgs.py for more

client = SoftLayer.Client(username=apiUsername, api_key=apiKey)
categoryObjectMask = "mask[isRequired, itemCategory[id, name]]"

configurations = client['Product_Package'].getConfiguration(
    id=package, mask=categoryObjectMask)

pricesObjectMask = "mask[id;item.description;categories.id]"

prices = client['Product_Package'].getItemPrices(
    id=package, mask=pricesObjectMask)

headerFormat = '%s - %s:'
priceFormat = '    %s -- %s'
for configuration in configurations:
    if (not configuration['isRequired']):
        continue
    print headerFormat % (configuration['itemCategory']['name'],
                          configuration['itemCategory']['id'])
    for price in prices:
        if ('categories' not in price):
            continue
        if any((category.get('id') == configuration['itemCategory']['id']
                for category in price['categories'])):
            print priceFormat % (price['id'], price['item']['description'])
