Authentication
**************

.. code-block:: python

    from vra_sdk.vra_config import VraConfig
    from vra_authenticate import VraAuthenticate
    from vra_sdk.vra_sdk import VraSdk

    VraConfig('my_config_file.json')

    # First i must create an VraAuthenticate object specifying an environment
    auth_obj = VraAuthenticate('UAT')
    # If i change my environment, the tenant and vcac_server attribute will be reloaded from the configuration file

    # Then i perform the actual authentication using login/password/domain...
    auth_obj.auth_login_password('my_login', 'my_password', 'my_domain')

    # ... or using a vRa token
    auth_obj.auth_login_token('my_login', 'my_token')

    # Once authenticated, i can create my vra_sdk_client using the authentication object
    my_vra_sdk = VraSdk(auth_obj, 'my_business_group')