.. PRC documentation master file, created by
   sphinx-quickstart on Fri Jan 24 09:19:19 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

######################################
Welcome to PRC's documentation!
######################################
.. automodule:: __init__
.. note::
       This is a BETA version.

******************
User Documentation
******************
**About postfix and rate limiting :**

.. toctree::
      :maxdepth: 4

   about_limit.rst

**Authentication:**

If you want to use the API, you must connecting you for each action (with login/password). You can use a token authentitication which you give an access to 600 seconds.

.. toctree::
      :maxdepth: 4

   login.rst
   token.rst

**URL available :**
  
  The default domain name of API is : **mxapi.YOURDOMAIN.com**

* ``/`` Root url, list the servers connected to PRC.
* ``/get-domains/`` Obtain the list of domains for a hostname.
* ``/get-values/`` Obtain the 3 MX values for a domain, for a hostname.
* ``/del-domain/`` Delete a domain (and all the MX values) for a hostname.
* ``/add-domain/`` Add a domain (and the 3 MX values). 
* ``/update-domain/`` Update the MX value for a domain.

*Document links* :

.. toctree::
      :maxdepth: 4

   get_domains.rst
   get_values.rst
   add_domain.rst 
   del_domain.rst
   update_domain.rst

**URL for transport :**
The optional transport table specifies a mapping from email addresses to message delivery transports and next-hop destinations.

* ``/get-transport/`` Obtain the list of extensions (fqdn) for a hostname and for a domain (not fqdn).
* ``/add-transport/`` Add a domain extension (if not exist).
* ``/del-transport/`` Delete a domain extension.

.. toctree::
   :maxdepth: 4

   get_transport.rst
   add_transport.rst
   del_transport.rst


************************
Developper Documentation
************************
**Modules available :**

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

