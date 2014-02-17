.. PRC documentation master file, created by
   sphinx-quickstart on Fri Jan 24 09:19:19 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
#######################
Authentication by Token
#######################

To avoid sending username and password with every request an authentication token can be requested, the duration is 600 secondes :

**For take the token :** 

.. code-block:: html

   curl -u USER:PASSWORD -i -X GET http://mxapi.YOURDOMAIN.com/api/token

**Return :**

.. code-block:: html

   HTTP/1.0 200 OK
   Content-Type: application/json
   Content-Length: 139
   Server: Werkzeug/0.9.4 Python/2.7.3
   Date: Thu, 28 Nov 2013 20:04:15 GMT

   {   
      "duration": 600,
      "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTM4NTY2OTY1NSwiaWF0IjoxMzg1NjY5MDU1fQ.eyJpZCI6MX0.XbOEFJkhjHJ5uRINh2JA1BPzXjSohKYDRT472wGOvjc"
   }

And now during the token validity period there is no need to send username and password to authenticate anymore:

.. code-block:: html

   $ curl -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTM4NTY2OTY1NSwiaWF0IjoxMzg1NjY5MDU1fQ.eyJpZCI6MX0.XbOEFJkhjHJ5uRINh2JA1BPzXjSohKYDRT472wGOvjc:x -i -X GET http://mxapi.YOURDOMAIN.com/URL
