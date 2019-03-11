Get/List data
***************

Once your definitions set, you can finally get/list your data.

Get data
=========

.. code-block:: python

    from pprint import pprint
    from vra_sdk.vra_config import VraConfig
    from vra_sdk.vra_authenticate import VraAuthenticate
    from vra_sdk.vra_sdk import VraSdk

    VraConfig('my_config_file.json')
    auth_obj = VraAuthenticate('UAT').auth_login_password('my_login', 'my_password', 'my_domain')
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
    Combining recursif and full data can cause a sever lack of performance

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

    from vra_sdk.vra_request import VraRequest
    VraRequest({}).get_object(object_type, key, value, limit, page, full)