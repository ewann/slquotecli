#currently this file holds some examples of server build
#using flex images - not yet replicated elsewhere

import SoftLayer
import os
#http://softlayer-python.readthedocs.org/en/latest/api/managers/vs.html
SL_API_USERNAME = os.environ.get("SL_API_USERNAME", None)
SL_API_KEY = os.environ.get("SL_API_KEY", None)

print SL_API_USERNAME
#print SL_API_KEY

client = SoftLayer.Client(username=SL_API_USERNAME, api_key=SL_API_KEY)

mgr = SoftLayer.VSManager(client)

# validated code

#options = mgr.get_create_options()
#print(options)

import pprint
#>>> stuff = ['spam', 'eggs', 'lumberjack', 'knights', 'ni']
#>>> stuff.insert(0, stuff[:])
pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(options)

new_vsi = {
    'domain': u'test01.labs.sftlyr.ws.local',
    'hostname': u'Meetup-27-instance2',
    'datacenter': u'mel01',
    'dedicated': False,
    'private': False,
    'cpus': 1,
#    'os_code' : u'CENTOS_LATEST',
    'image_id': 'd45425f5-9155-4302-83c7-64fc9d94b747',
    'hourly': True,
#    'ssh_keys': [1234],
#    'disks': ('25'),
#    'disks': ('100','25'),
    'local_disk': True,
    'memory': 1024,
    'tags': 'test, pleaseCancel'
}

'''
 {   'itemPrice': {   'hourlyRecurringFee': '0',
                                             'item': {   'description': '25 GB (LOCAL)'},
                                             'recurringFee': '0'},
                            'template': {   'blockDevices': [   {   'device': '0',
                                                                    'diskImage': {   'capacity': 25}}],
                                            'id': '',
                                            'localDiskFlag': True}},
                        {   'itemPrice': {   'hourlyRecurringFee': '.006',
                                             'item': {   'description': '100 GB (LOCAL)'},
                                             'recurringFee': '4'},
                            'template': {   'blockDevices': [   {   'device': '0',
                                                                    'diskImage': {   'capacity': 100}}],
'''

vsi = mgr.verify_create_instance(**new_vsi)
vsi = mgr.create_instance(**new_vsi)
# vsi will have the newly created vsi details if done properly.
pp.pprint(vsi)

options = mgr.get_create_options()
#pp.pprint(options)


#for vsi in mgr.list_instances():
    #print vsi

#vsi = mgr.get_instance(13300821)
#print vsi['blockDevices']

#mgr.cancel_instance(13140633)
