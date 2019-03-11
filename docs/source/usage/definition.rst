Definitions
*************

To perform get/list operation against your vRa infrastructure, you must first create definitions of your vRa objects.
vra_sdk will then use your definition inside his `factory <https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Factory.html>`_

Definitions are basically python class that describe your object attributes.

Declare these object is the only cost you'll have using this library. However it must usually be do only once.

To declare a model definition you must:

- Declare your new models in your configuration file in the *business_models sections*.
- Create the related python class

Config file
============

Here is an example of declaration pf a definition of a class name *Vm* in the module *vra_vm*, in the folder *definitions/models*

.. code-block:: json

    {
        "business_models": {
        "vm": {
            "path": "definitions.models.vra_vm.Vm"
            }
        }
    }

The key (in the example *vm*) is the key you'll use later while requesting data against your vRa infrastructure (Warning: the key *payload* is reserved)

*path* is the path to your business models definitions (using the python syntax folder.module.class)
The path is relative to the python execution folder. Relative path are accepted.

Definition creation
====================

During the creation of one object, every kwargs used to create an object must be part of the class signature (it can have less but not more)

One example of a definition can be found in the `data_examples folder <https://github.com/richarddevers/vrasdk/blob/master/examples/definitions/vra_vm.py>`_

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

Definition creation helpers
===========================
To know which attributes must set, you can use the **vra_sdk.get_raw_definition** method. This methods will return you a dict of prettify vRa data that you'll just have to defined in your class attributes.

eg:

.. code-block:: python

    from pprint import pprint
    from vra_sdk.vra_config import VraConfig
    from vra_sdk.vra_authenticate import VraAuthenticate
    from vra_sdk.vra_sdk import VraSdk

    VraConfig('my_config_file.json')
    auth_obj = VraAuthenticate('UAT').auth_login_password('my_login', 'my_password', 'my_domain')
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
