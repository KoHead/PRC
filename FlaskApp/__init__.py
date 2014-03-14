# -*- coding: utf-8 -*-
"""Postfix Rate Control is an API REST coding in python
   :synopsis: This API can update the MX configuration of postfix server connected to PCR.
   ..moduleauthor:: Damien Mathieu <damien.mathieu@adthink-media.com>
"""
from system import return_listserver, return_domains, return_domain_values, return_domain_deleted, return_domain_added, return_domain_updated, return_get_transport, return_add_transport, return_del_transport, return_del_queue

from flask import Flask, abort, request, jsonify, g, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

app = Flask(__name__)

app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# extensions
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@app.route('/api/users', methods = ['POST'])
def new_user():
    """Register a new user
       Args:
	int. : User id
       Raises:
        error_code. : error http code 400
    """
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}

@app.route('/api/users/<int:id>')
def get_user(id):
    """Return the username of user.
       URL Structure with curl:
             curl -i -X POST -H "Content-Type: application/json" -d '{"username":"miguel","password":"python"}' http://127.0.0.1:5000/api/users
       Args:
	int. : User id
       Raises:
        error_code. : error http code 400
    """
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({ 'username': user.username })

@app.route('/api/token')
@auth.login_required
def get_auth_token():
    """Return a token for the nexts authentications. The period of validity of token is defined by the duration variable
       Returns:
        token. : Token string
    """
    duration = 600
    token = g.user.generate_auth_token(duration)
    return jsonify({ 'token': token.decode('ascii'), 'duration': duration })


@app.route('/')
@auth.login_required
def main_page():
    """Return server list of servers connected to api. (server available)
       Returns:
	list. : Server list available (from servers_list.txt)
       Raises:
	str. : Error message
    """
    #We get the current username
    username = str(g.user.username)
    #And we give this username to "return_listserver". The goal is determinate the Business Unit of current user
    list_server=return_listserver(username)
    return jsonify(results=list_server)

@app.route("/get-domains/<hostname>")
@auth.login_required
def get_domains(hostname):
    """Return a list of domains for a hostname (in args)
      URL Structure:
		/getdomains/<hostname>
      Args:
	hostname (str) : The hostname
      Returns:
        list. : Domains list
       Raises:
        str. : Error message
    """
    #We get the current username
    username = str(g.user.username)
    #And we give this username to "return_listserver". The goal is determinate the Business Unit of current user
    result_domains=return_domains(hostname, username)
    return jsonify(results=result_domains)

@app.route("/get-values/<hostname>/<domain_name>")
@auth.login_required
def get_domain_value(hostname,domain_name):
    """Return MX values for a domain from a hostname
       URL Structure:
		/getvalues/<hostname>/<domain_name>
       Args:
        hostname (str) : The hostname
	domain_name (str) : The domain name
       Returns:
        list. : List of Mx values ::
		[1] -- destination_concurrency_limit
		[2] -- destination_rate_delay
		[3] -- destination_recipient_limit
       Raises:
        str. : Error message
    """
    #We get the current username
    username = str(g.user.username)
    #And we give this username to "return_listserver". The goal is determinate the Business Unit of current user
    result_value=return_domain_values(hostname, domain_name, username)
    return jsonify(results=result_value)

@app.route("/del-domain/<hostname>/<domain_name>")
@auth.login_required
def del_domain(hostname,domain_name):
    """Delete a domain (and all the MX values in main.cf and master.cf)
       URL Structure:
		/deldomain/<hostname>/<domain_name>
       Args:
        hostname (str) : The hostname
        domain_name (str) : The domain name
       Returns:
	str. : Succes message or error message.
    """
    #We get the current username
    username = str(g.user.username)
    #And we give this username to "return_listserver". The goal is determinate the Business Unit of current user
    result_value=return_domain_deleted(hostname, domain_name, username)
    return jsonify(results=result_value)

@app.route("/add-domain/<hostname>/<domain_name>/<int:value1>/<int:value2>/<int:value3>")
@auth.login_required
def add_domain(hostname, domain_name, value1, value2, value3):
    """ Add a domain (if does not exist) and the MX values
	URL Structure:
		/add-domain/<hostname>/<domain_name>/<int:value1>/<int:value2>/<int:value3>
	Args:
	 hostname (str) : The hostname
         domain_name (str) : The domain name
	 value1 (int) : destination_concurrency_limit (ex: 60)
	 value2 (int) : destination_recipient_limit (ex: 20)
         value3 (str) : destination_rate_delay (ex: 1) (seconds)
	Returns:
	 str. : Succes message or error message (domain already exist)
    """
    #We get the current username
    username = str(g.user.username)
    #And we give this username to "return_listserver". The goal is determinate the Business Unit of current user
    result=return_domain_added(hostname, domain_name, value1, value2, value3, username)
    return jsonify(results=result)

@app.route("/update-domain/<hostname>/<domain_name>/<int:value1>/<int:value2>/<int:value3>")
@auth.login_required
def update_domain(hostname, domain_name, value1, value2, value3):
    """ Add a domain (if does not exist) and the MX values
        URL Structure:
                /update-domain/<hostname>/<domain_name>/<value1>/<value2>/<value3>
        Args:
         hostname (str) : The hostname
         domain_name (str) : The domain name
         value1 (int) : destination_concurrency_limit (ex: 60)
         value2 (int) : destination_recipient_limit (ex: 20)
         value3 (str) : destination_rate_delay (ex: 1s)
        Returns:
         str. : Succes message or error message (domain already exist)
    """
    #We get the current username
    username = str(g.user.username)
    #And we give this username to "return_listserver". The goal is determinate the Business Unit of current user
    result=return_domain_updated(hostname, domain_name, value1, value2, value3, username)
    return jsonify(results=result)

@app.route("/get-transport/<hostname>/<domain_name>")
@auth.login_required
def get_transport(hostname, domain_name):
    """ Add a domain (if does not exist) and the MX values
        URL Structure:
                /get-transport/<hostname>/<domain_name>
        Args:
         hostname (str) : The hostname
         domain_name (str) : The domain name
        Returns:
         str. : Succes message or error message (domain does not exist)
    """
    #We get the current username
    username = str(g.user.username)
    #And we give this username to "return_listserver". The goal is determinate the Business Unit of current user
    result=return_get_transport(hostname,domain_name, username)
    return jsonify(results=result)

@app.route("/add-transport/<hostname>/<domain_name>/<domain_extension>")
@auth.login_required
def add_transport(hostname, domain_name, domain_extension):
    """ Add a domain (if does not exist) in transport file
        URL Structure:
                /add-transport/<hostname>/<domain_name>/<domain_extension>
        Args:
         hostname (str) : The hostname
         domain_name (str) : The domain name (not fqdn)
	 domain_extension (str) : The domain name with the extension (fqdn)
        Returns:
         str. : Succes message or error message (domain extension already exist)
    """
    #We get the current username
    username = str(g.user.username)
    #And we give this username to "return_listserver". The goal is determinate the Business Unit of current user
    result=return_add_transport(hostname, domain_name, domain_extension, username)
    return jsonify(results=result)


@app.route("/del-transport/<hostname>/<domain_name>/<domain_extension>")
@auth.login_required
def del_transport(hostname, domain_name, domain_extension):
    """ Delete a domain extension (if exist) for a domain name in transport file
        Args:
         hostname (str) : The hostname
         domain_name (str) : The domain name (not fqdn)
         domain_extension (str) : The domain name with the extension (fqdn)
        Returns:
         str. : Succes message or error message (domain extension does not exist)
    """
    #We get the current username
    username = str(g.user.username)
    #And we give this username to "return_listserver". The goal is determinate the Business Unit of current user
    result=return_del_transport(hostname, domain_name, domain_extension, username)
    return jsonify(results=result)


@app.route("/del-queue/<hostname>")
@auth.login_required
def del_queue(hostname):
    """ Delete the postfix queue
    """
    #We get the current username
    username = str(g.user.username)
    esult=return_del_queue(hostname, username)
    eturn jsonify(results=result)

if __name__ == '__main__':
    """ Launch flask server
    """
    app.debug=True
    app.run()
