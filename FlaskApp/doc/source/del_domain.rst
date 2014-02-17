.. PRC documentation master file, created by
   sphinx-quickstart on Fri Jan 24 09:19:19 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
############
/del-domain/
############

**Delete Domain**

You can delete a domain with this url. Beware, the rate values will also be erased.

.. toctree::
   :maxdepth: 4


URL :
-----

.. code-block:: html

   http://mxapi.YOURDOMAIN.com/del-domain/hostname/domain_name/

**Values :** 
        * ``hostname`` The hostname of postfix server.
        * ``domain_name`` The domain name to be erased.

.. warning:: The domain_name is not FQDN here. 

Example :
---------

.. code-block:: html

   http://mxapi.YOURDOMAIN.com/del-domain/YOURHOSTNAME/gmail

Delete the gmail domain from main.cf and master.cf on the host YOURHOSTNAME the values, **destination_concurrency_limit**, **destination_recipient_limit**, **destination_rate_delay** will also be erased. 
