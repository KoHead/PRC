.. PRC documentation master file, created by
   sphinx-quickstart on Fri Jan 24 09:19:19 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
#############################
/get-transport/
#############################
**Get domain's list from the postfix's transport file**
You can obtain all the extensions matched for a domain name in postfix

.. toctree::
   :maxdepth: 4


URL :
-----

.. code-block:: html

   http://mxapi.YOURDOMAIN.com/get-transport/hostname/domain_name/

**URL parms :** 
        * ``hostname`` The hostname of postfix server.
        * ``domain_name`` Your new domain name.

.. warning:: The domain_name is not fqdn here. 

**Return Values :**

A list of domain name with extensions.

Example :
-----

.. code-block:: html

   http://mxapi.YOURDOMAIN.com/get-transport/YOURHOSTNAME/yahoo

Return the extensions of domain yahoo from YOURHOSTNAME :

* talk21.com
* yahoo.fr
* yahoo.com
* ymail.com
* yahoo.co.uk
* rocketmail.com
* yahoo.ca
* yahoo.com.mx
* yahoo.de
* yahoo.es
* yahoo.com.br
* yahoo.it
* y7mail.com
* yahoo.no
* yahoo.cn
* yahoo.ro
* yahoo.co.in
* yahoo.co.id
* yahoo.co.nz
* yahoo.in
* yahoo.co.jp
* yahoo.com.vn
* yahoo.dk
* yahoo.gr
* yahoo.com.au
* yahoo.com.ar
* yahoo.com.cn
* yahoomail.com
* btinternet.com
* yahoo.com.co
* yahoo.com.ph
* geocities.com
* yahoo.ie
* yahoo.com.sg
* bellsouth.net
* yahoo.com.tr
* yahoo.se
* yahoo.pl
* yahoo.co.th
* yahoo.com.tw
* ameritech.net
* verizon.net
* yahoo.nl
* yahoo.co.kr
* yahoo.jp
* yahoo.com.hk
* att.net
* yahoo.com.my
* kimo.com
* yahoo.fi
* btopenworld.com
* yahoo.cl
* xtra.co.nz
* flash.net
* swbell.net
* wans.net
* yahoo.com.pe
* yahoo.com.ve
* yahooxtra.co.nz
