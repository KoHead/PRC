.. PRC documentation master file, created by
   sphinx-quickstart on Fri Jan 24 09:19:19 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
#################
/get-domains/
#################
**Get domain's list**

You can obtain a domain's list with this url. This list describe the domains for which the rate limiting is activate.

.. toctree::
   :maxdepth: 4


URL :
-----

.. code-block:: html

   http://mxapi.YOURDOMAIN.com/get-domains/hostname

**Values :** 
        * ``hostname`` The hostname of postfix server.

.. warning:: The domain_name is not fqdn here. 


Example :
-----

.. code-block:: html

   http://mxapi.YOURDOMAIN.com/add-domain/YOURHOSTNAME/

Return the list of affected domains by rate limiting for YOURHOSTNAME

* ``destination_concurrency_limit`` = 10
* ``destination_recipient_limit`` = 10
* ``destination_rate_delay`` = 1s
