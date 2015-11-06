
import SoftLayer
import os
#http://softlayer-python.readthedocs.org/en/latest/api/managers/vs.html
SL_API_USERNAME = os.environ.get("SL_API_USERNAME", None)
SL_API_KEY = os.environ.get("SL_API_KEY", None)

SL_ACCOUNT = ''

print SL_API_USERNAME
print SL_API_KEY

client = SoftLayer.Client(username=SL_API_USERNAME, api_key=SL_API_KEY)


from pprint import pprint as pp
apiUsername = SL_API_USERNAME
apiKey = SL_API_KEY

#https://gist.github.com/underscorephil/4067388
def getImageTemplateId(templateName):
    client = SoftLayer.Client(username=apiUsername, api_key=apiKey)
    templates = client['Account'].getBlockDeviceTemplateGroups()

    for template in templates:
        if template['name'] == templateName:
            return template['globalIdentifier']


pp(getImageTemplateId('packer-centos-6-demo'))


import SoftLayer.API
from pprint import pprint as pp

api_username = SL_API_USERNAME
api_key = SL_API_KEY

hostname = 'pjackson-video'
domain_name = 'example.com'

client = SoftLayer.Client(
    username=api_username,
    api_key=api_key,
)

guest = {}
guest['datacenter'] = "mel01"
guest['startCpus'] = 1
guest['maxMemory'] = 1024
guest['localDiskFlag'] = False
guest['hostname'] = hostname
guest['domain'] = domain_name
guest['hourlyBillingFlag'] = False
#guest['imageTemplateId'] = pp(getImageTemplateId('packer-centos-6-demo'))
guest['blockDeviceTemplateGroup'] = '796067' #{'globalIdentifier': "796065"}
#result = client['Virtual_Guest'].createObject(guest)

#result = client['Virtual_Guest'].createObject(guest)
#import inspect

#inspect.getmembers(client)

#pp(result)

#pp(client.__dict__)



#http://sldn.softlayer.com/blog/phil/Dedicated-server-ordering-Flex-Image-and-Python
