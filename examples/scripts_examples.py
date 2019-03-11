from vra_sdk.vra_config import VraConfig
from vra_sdk.vra_authenticate import VraAuthenticate
from vra_sdk.vra_sdk import VraSdk
import os
from pprint import pprint as pprint

# credential loading from environment var
domain = "foo.fuu.com"
environment = os.environ['vra_environment']
login = os.environ['vra_login']
password = os.environ['vra_password']
######

# authentication part
VraConfig('config.json')
auth = VraAuthenticate(environment).auth_login_password(
    login, password, domain)
my_business_group = 'my_bg_name'
my_client = VraSdk(auth, my_business_group)
######

# get data on one vm from name
vm_name = 'my_vm_name'
vm_data = my_client.get_data('vm', 'name', vm_name)[0]
print(vm_data.id)
######

# get data on one vm from id
vm_id = 'my_vm_id'
vm_data = my_client.get_data('vm', 'id', vm_id)
print(vm_data.name)

# you can either get the data as dict or as json
pprint(vm_data.to_json())
pprint(vm_data.to_dict())
######

# get list of vm
vm_list = my_client.get_data('vm', None, None)
for vm in vm_list:
    print(vm.name)

######

# request a resource action
param = {"my_param_key": "my_param_value"}
req = my_client.request_resource_action("My_resource_action_name", vm_data.id, **param)
pprint(req.payload.customized)  # hake a look at the payload (by default vRa7 format)
req.execute_async()  # execute the request without hanging
pprint(req.status_url)  # get the request status url
######

# request a catalog item
param = {
    "NbMachine": 1,
    "LeaseDays": 1,
    "Environment": "DEV",
    "Size": "",
    "DataDiskSize": 20,
}
# if i have added 'payload_version':6 to my param dict, the request would have generate a vRa6 payload object
# doing so, the 'provider-' prefix would have been added automatically(or not if it's already set)


def my_payload_customization(payload, **kwargs):
    # for some business reason, i need to add the business group id to the data section of my payload
    # i can perform it (or any needed customization) inducing a payload customization function this way
    # kwargs contain data you can found in the 'not_in_data' section of your configuration file
    # note that that it depends of the context (not the same data if you request a catalog item or a resource action)
    payload['data']['business_group_id'] = kwargs['business_group_id']
    return payload


create_vm_request = my_client.request_catalog_item('My Awesome RHEL', my_payload_customization, **param)
pprint(create_vm_request.payload.customized)  # have a look at the payload
req = create_vm_request.execute_sync(),  # execute it synchronously, the script will wait for either a fail or success of the request by polling the status url regularly
######
