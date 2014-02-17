.. PRC documentation master file, created by
   sphinx-quickstart on Fri Jan 24 09:19:19 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
############
/add-transport/
############

**Add a domain extension for a domain name**

You can add a domain extenion with this url. You must specify the domain extension AND the domain name in the url.

.. toctree::
   :maxdepth: 4

URL :
-----

.. code-block:: html

   http://mxapi.YOURDOMAIN.com/add-transport/hostname/domain_name/domain_name_extension

**Values :** 
        * ``hostname`` The hostname of postfix server.
        * ``domain_name`` The domain name. (Not FQDN)
        * ``domain_name_extension`` The domain name with the extension you want. (FQDN)

Example :
---------

.. code-block:: html

   http://mxapi.YOURDOMAIN.com/add-transport/YOURHOSTNAME/gmail.com/gmail

Will add the **.com** extension for the domain **gmail**.
