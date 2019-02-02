Overview
========
vra_sdk is a python library used to simplify basic interaction with VmWare vRealize Automation.

It provides the following features:

- Automatic payload creation for vRa6 and vRa7
- Automatic catalog/entitlement management
- List resources
- Get data on a specific resource
- For list/get, allow to get the raw vRa response or a more user friendly response
- Request a catalog item
- Request a resource action
- Easyly handle any vRa resource type (even dynamic type)

Even if as a library, you can use whatever functionallity exposed, the 4 most important are the following
- vra_sdk.get_data
- vra_sdk.list_data
- vra_sdk.request_catalog_item
- vra_sdk.request_resource_action