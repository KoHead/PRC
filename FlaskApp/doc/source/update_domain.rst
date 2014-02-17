.. PRC documentation master file, created by
   sphinx-quickstart on Fri Jan 24 09:19:19 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
###############
/update-domain/
###############

**Update rate limiting value for a domain**

You can update the rate values of domain with this url. You must give the rate values.

.. toctree::
   :maxdepth: 4


URL :
-----

.. code-block:: html

   http://mxapi.YOURDOMAIN.com/add-domain/hostname/domain_name/destination_concurrency_limit/destination_recipient_limit/destination_rate_delay

**Values :** 
        * ``hostname`` The hostname of postfix server.
        * ``domain_name`` Your new domain name.

.. warning:: The domain_name is not fqdn here. 

.. warning:: If you want update the default values, use "default" as domain_name.


* ``destination_concurrency_limit`` This decides the initial number of parallel deliveries. Default is 5, you don't want that probably, so set it as 1.
* ``destination_recipient_limit`` This decides the number of recipients per mail delivery. Setting this parameter to a value of 1 changes the meaning of the corresponding per-destination concurrency limit from concurrency per domain into concurrency per recipient. So set this to 2. This will take care of the domain. If you set it to 1, throttling will work only if you send mails to the same recipient and not for the same recipient domain.
* ``destination_rate_delay/`` This defines the delay between individual deliveries to the destination using this transport. Set this as per required. Suppose you want 10 deliveries per minute to gmail, then you can set it up like 60/10 = 6s.


.. note:: If the domain does not exist, the returns is : " This domain does not exist, you can't update it" 

Example :
---------

.. code-block:: html

   http://mxapi.YOURDOMAIN.com/update-domain/YOURHOSTNAME/gmail/10/10/1

Will update the gmail domain rate values to the host YOURHOSTNAME with :

* ``destination_concurrency_limit`` = 10
* ``destination_recipient_limit`` = 10
* ``destination_rate_delay`` = 1s
