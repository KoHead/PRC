.. PRC documentation master file, created by
   sphinx-quickstart on Fri Jan 24 09:19:19 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
#################################
Postfix and rate limiting methods
#################################

**Rate limiting presentation in Postfix**

Postfix use 3 parameters for limit the senders. You can specify different value for each domains

**Values :** 

* ``destination_concurrency_limit`` This decides the initial number of parallel deliveries. Default is 5, you don't want that probably, so set it as 1.
* ``destination_recipient_limit`` This decides the number of recipients per mail delivery. Setting this parameter to a value of 1 changes the meaning of the corresponding per-destination concurrency limit from concurrency per domain into concurrency per recipient. So set this to 2. This will take care of the domain. If you set it to 1, throttling will work only if you send mails to the same recipient and not for the same recipient domain.
* ``destination_rate_delay/`` This defines the delay between individual deliveries to the destination using this transport. Set this as per required. Suppose you want 10 deliveries per minute to gmail, then you can set it up like 60/10 = 6s.

**Default Values :**

* ``default_destination_concurrency_limit`` The default maximal number of parallel deliveries to the same destination. Used if the domain is not matched by all the others rules.
* ``default_destination_rate_delay`` The default amount of delay that is inserted between individual deliveries to the same destination; the resulting behavior depends on the value of the corresponding per-destination recipient limit. 
* ``default_destination_recipient_limit``  The default maximal number of recipients per message delivery. 

So, when you configure a new server. You must specify the 3 defaults values, and your specific values per domain. Beware that your domain has to be registered in the transport file.

**The transport parameters :**

You must also checked if your domain extentions is matched in transport file of postfix. The file links all the extension for a domain to domain name.

Extract of transport file :

.. code-block:: html

        yahoo.fr           yahoo:
        yahoo.com           yahoo:

Yahoo.fr and yahoo.com used yahoo domain name. So the values:

* ``yahoo_destination_concurrency_limit`` = 40
* ``yahoo_destination_rate_delay`` = 1s
* ``yahoo_destination_recipient_limit`` = 2

Are used for yahoo.fr and yahoo.com
