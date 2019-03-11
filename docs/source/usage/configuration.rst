Configuration
***************

VraSdk configuration is done using json file.

You can find a template for this configuration file the `data_examples <https://github.com/richarddevers/vra_sdk/blob/master/examples/config_template.json>`_ folder.

The most minimalist example can be also found in the same place (minimal_config.json).
However, with this one, you'll only be able to request catalog item or resource action (since no business_models are defined, you won't be able to get/list any data from your vRa infrastructurel)

Configuration file fields
=========================

**vcac_servers:** Map of vcac_servers per environment

**tenant:** Map of tenant per environment

**catalog_item:**: Data structure used to defined catalog item custom data.

**resource_ation:**: Map to define custom resource action.

**business_models:** Used to defined path to vRa type definitions.

**payload_default_version:** Default version of the payload to create to interact with vRa (catalog item creation and resource action)

**timeout:** `Request timeout value <http://docs.python-requests.org/en/master/user/quickstart/#timeouts>`_

**verify:** `Request's session verify value <http://docs.python-requests.org/en/master/_modules/requests/sessions/?highlight=verify>`_

**max_vra_result_per_page:** Max result per page for vRa request. Used for recursif call. On vRa 6 and 7, this limit is 5000.

**not_in_data:** Fields to be ommit in payload creation. These fields are still available when using payload customization method

Load your configuration
=======================

To load a configuration file in your script/app , just create a VraConfig object specifying his configuration file.

Since this object is a singleton it will be create each time a module need it but it will use the same object your firstly create.

If needed, you can reactive the __init__ of this class by settings the _sealed attribute to False

Note that the path is relative to the python execution folder. Relative path are supported.

.. code-block:: python

   from vra_sdk.vra_config import VraConfig

   VraConfig('your/path/to/config.json')

   # deactivating the singleton effect for next call
   VraConfig()._sealed=False 
