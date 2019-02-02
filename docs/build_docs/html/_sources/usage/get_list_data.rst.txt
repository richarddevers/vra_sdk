.. _my-reference-label:

Get/List data
***************

Models definitions
====================

To perform get/list operation against your vRa infrastructure, you must first create definitions of your vRa objects.
vra_sdk will then use your definition inside his `factory <https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Factory.html>`_

Definitions must be declared in your config json file in the business_models sections.

The key (in the below example 'vm') is the key you'll use later while requesting data against your vRa infrastructure (Warning: the key 'payload'is reserved)

*path* is the path to your business models definitions (using the python syntax folder.module.class)
The path is relative to the python execution folder. Relative path are accepted.

When *enforce_id* is set to true, during the creation of one object, every kwargs used must be part of the class signature (they can be less but not more)

.. code-block:: json

    {
        "business_models": {
        "vm": {
            "path": "definitions.models.vra_vm.Vm",
            "enforce_id": true
            }
        }
    }

One example of a definition can be found in the `data_examples folder <https://github.com/richarddevers/vrasdk/blob/master/data_examples/definitions/vra_vm.py>`_

Let analyze this example:

.. code-block:: python

    from vra_sdk.models.vra_object import VraBaseObject

*VraBaseObject* is a very small class that will implement helpers for `to_dict and to_json method <https://github.com/richarddevers/vrasdk/blob/master/vra_sdk/models/vra_object.py>`_

.. code-block:: python

    RESOURCE_TYPE = ['Virtual Machine']

This array of string must contains the name of your resource type. This types will be used to create vra `Odata url filters <https://vdc-download.vmware.com/vmwb-repository/dcr-public/d2e4e058-df27-4ac1-a100-4dfd0ef774c0/cb3a080c-8e25-4492-9f1e-ff923ec1b98c/tips.html>`_
You can specify multiple type for one object class

.. code-block:: python

    class Vm(VraBaseObject):

        def __init__(self, raw_data=None, id=None, name=None ...

Here i define my vRa object. The attribute *raw_data* is **required**. Every other attributes are free but must be returned by your vRa infrastructure.
This definitions also serves you as documentation. If needed you can also implement specific method/mechanism

To know which attributes must be set, you can use the **vra_sdk.get_raw_definition** method. This methods will return you a dict of prettify vRa data that you'll just have to defined in your class attributes.

eg:

.. code-block:: python

    from pprint import pprint
    from vra_sdk.vra_config import VraConfig
    from vra_authenticate import VraAuthenticate
    from vra_sdk.vra_sdk import VraSdk

    VraConfig('my_config_file.json')
    auth_obj = VraAuthenticate().auth_login_password('my_login', 'my_password', 'my_domain')
    my_vra_sdk = VraSdk(auth_obj, 'my_business_group')

    # eg for VirtualMachine type
    pprint(my_vra_sdk.get_raw_definition('name', 'my_vm_name', 'Virtual Machine'))

    >>{'name':'my_vm_name',
    >>'id':'my_vm_id',
    >>'attr1':['aatr1'],
    >>'attr2':{'attr2':'value'}
    >>}

With that kind of very basic example, the class *Vm* in *definitions/models/vra_vm.py* (as defined in the configuration file above) should look like this:

.. code-block:: python

    # -*- coding: utf-8 -*-
    from vra_sdk.models.vra_object import VraBaseObject

    RESOURCE_TYPE = ['Virtual Machine']
    class Vm(VraBaseObject):

        def __init__(self, raw_data=None, name=None, id=None, attr1=None, attr2=None)
            super().__init__()
            self.raw_data=raw_data
            self.name=None
            self.id=None
            self.attr1=attr1 or []
            self.attr2=attr2 or {}

Get data
=========
Once your definitions set, you can finally get/list your data.

.. code-block:: python

    from pprint import pprint
    from vra_sdk.vra_config import VraConfig
    from vra_authenticate import VraAuthenticate
    from vra_sdk.vra_sdk import VraSdk

    VraConfig('my_config_file.json')
    auth_obj = VraAuthenticate().auth_login_password('my_login', 'my_password', 'my_domain')
    my_vra_sdk = VraSdk(auth_obj, 'my_business_group')

    # Here i look for a 'vm' type object (as set in my config file)
    # where 'name' is equal to 'my_vm'
    vm_data = my_vra_sdk.get_data('vm', 'id', 'vm_id')

    # Now i can acces to my object attribute defined in my definition
    print(vm_data.name)
    print(vm_data.id)

    # I can also acces to the vRa raw result
    pprint(vm_data.raw_result)

    # I can use the VraObject method to either export a dict or a json string with all the data
    pprint(vm_data.to_dict())
    pprint(vm_data.to_json())

List data
=========
You can use the list_data() function from the vra_sdk module if you expect to have more than one result

.. code-block:: python

    vm_list = my_vra_sdk.list_data('vm', None, None, None, 1, False, True)
    for vm in vm_list:
        print(vm.name)

Warning:
    list_data() function allow to perform either a recursif/simple call and full data/light data at the same time.
    Combining recursif and full data can cause a server lack of performance

    The full option will add for each discovered item a supplementary call.

    So if your vRa infrastructure return 4000 objects, this will result in the following:
        - 1 call to list the 4000 object
        - 4000 call to get details on each

    Another example, if vRa return 8000 objects:
        - 2 call to get the 8000 objects (vRa paginate result up to 5000 item per page max)
        - 8000 call to get the details

    Use it wisely!


Advanced method
===============
get_data() and list_data() are just wrapper of the same function get_object() from the vra_request module.
If needed, you can directly use it this way:


.. code-block:: python

    from vra_request import VraRequest
    VraRequest({}).get_object(object_type, key, value, limit, page, full)