PRC
===

Postfix Rate Control REST API
.. Adthink-Mx documentation master file, created by
   sphinx-quickstart on Fri Jan 24 09:19:19 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

######################################
Welcome to PRC 's documentation!
######################################
.. automodule:: __init__
.. note::
       This is a BETA version.

******************
User Documentation
******************
**About postfix and rate limiting :**

http://www.postfix.org/TUNING_README.html

**Authentication:**

If you want to use the API, you must connecting you for each action (with login/password). You can use a token authentitication which you give an access to 600 seconds.


**URL available :**


* ``/`` Root url, list the servers connected to Adthink-Mx.
* ``/get-domains/`` Obtain the list of domains for a hostname.
* ``/get-values/`` Obtain the 3 MX values for a domain, for a hostname.
* ``/del-domain/`` Delete a domain (and all the MX values) for a hostname.
* ``/add-domain/`` Add a domain (and the 3 MX values). 
* ``/update-domain/`` Update the MX value for a domain.




