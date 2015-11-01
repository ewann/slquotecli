#!/usr/bin/python
import SoftLayer
import pprint

# Get the SoftLayer API client object
#client = SoftLayer.Client(username=myuser, api_key=mykey, endpoint_url=SoftLayer.API_PUBLIC_ENDPOINT)
client = SoftLayer.create_client_from_env(timeout=240)

# Get the list of packages
pkgs = client['Product_Package'].getAllObjects(mask='id, name')
pprint.pprint(pkgs)
