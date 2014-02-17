.. PRC documentation master file, created by
   sphinx-quickstart on Fri Jan 24 09:19:19 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

###############
/del-transport/
###############

**Delete Domain from the transport file**

You can delete a domain extension for a domain name with this url.

.. toctree::
   :maxdepth: 4


URL :
-----

.. code-block:: html

        http://mxapi.YOURDOMAIN.com/del-transport/hostname/domain_name/domain_name_extension

**Values :** 
        * ``hostname`` The hostname of postfix server.
        * ``domain_name`` The domain name. (Not FQDN)
        * ``domain_name_extension`` The domain name with the extension you want. (FQDN)
Example :
---------

.. code-block:: html

   http://mxapi.YOURDOMAIN.com/del-transport/YOURHOSTNAME/gmail.it/gmail

Delete the **gmail.it** domain extension for the domain name **gmail**.

