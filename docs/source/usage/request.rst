Perform request
*********************

Request a catalog item
======================
.. code-block:: python

    from pprint import pprint
    from vra_sdk.vra_config import vra_config
    from vra_authenticate import VraAuthenticate
    from vra_sdk.vra_sdk import VraSdk

    VraConfig('my_config_file.json')
    auth_obj = VraAuthenticate('UAT').auth_login_password('my_login', 'my_password', 'my_domain')
    my_vra_sdk = VraSdk(auth_obj, 'my_business_group')

    # Defining my resquest parameters as defined in my asd 
    param = {
        "NbMachine": 1,
        "LeaseDays": 1,
        "Environment": "DEV",
        "Size": "",
        "DataDiskSize": 20,
    }

    # i create a request object. At this time no request have been actually performed
    create_vm_request = my_vra_sdk.request_catalog_item('My Awesome centos', **param)
    pprint(create_vm_request.payload.customized)  # have a look at the payload
    
    # i execute my request. The script will wait for either a fail or success of the request by polling the status url regularly
    # i could have execute it without hanging the terminal using execute_async()
    req = create_vm_request.execute_sync()

Request a resource action
=========================

.. code-block:: python

    from pprint import pprint
    from vra_sdk.vra_config import vra_config
    from vra_authenticate import VraAuthenticate
    from vra_sdk.vra_sdk import VraSdk

    VraConfig('my_config_file.json')
    auth_obj = VraAuthenticate('my_environment').auth_login_password('my_login', 'my_password', 'my_domain')
    my_vra_sdk = VraSdk(auth_obj, 'my_business_group')

    # Resource action parameter creation
    param = {"my_param_key": "my_param_value"}
    req =my_vra_sdk.request_resource_action("My_resource_action_name", vm_data.id, **param)

    pprint(req.payload.customized)  # have a look at the payload

    req.execute_async()  # execute the request without hanging
    pprint(req.status_url)  # get the request status url

Payload customization
=====================
If you need to perform specific customization to you payload, you can perform it creating a customization function as in the example below:

.. code-block:: python

    def my_payload_customization(payload, **kwargs):
        payload['data']['business_group_id'] = kwargs['business_group_id']
        return payload


    # I use payload customization for a catalog item request
    create_vm_request = my_vra_sdk.request_catalog_item('My Awesome centos', my_payload_customization, **param)
    # For a resource action request
    resource_action_request =my_vra_sdk.request_resource_action("My_resource_action_name", vm_data.id, my_payload_customization, **param)

From within the customization function, you can access interesting data from the kwargs:

kwargs available for every request:
 * tenant_name
 * business_group_id
 * business_group_name
 * payload_type
 * payload_version
 * requested_for

kwargs available for catalog item request:
 * catalog_item_id
 * catalog_item_name

kwargs available for resource action request:
  * resource_action_name
  * resource_action_id
  * resource_id

Payload version
===============
For every request, if you add the key 'payload_version':6 to the parameter dict, the request is generated using vRa6 payload object

Doing so, the 'provider-' prefix is added automatically (or not if it's already set)

Request execution url/method is also custom to each version.

Payload enforcement
===================
You can defined specific payload json file for each catalog item/resource action request.

You can defined it using the configuration file

.. code-block:: json

    {  "catalog_item": {
            "My catalog item name": {
                "payload": "v7/vm/catalog_item_example.json"
                }
            }
        "resource_action": {
            "My resource action name": {
                "payload": "v7/vm/resource_action_example.json"
                }
        }
    }

Payload path are relative to your python execution folder. Relative path are authorized.

Parameter specified during request creation will be added to the data/item parts of the payload.

Payload customization function are compatible.