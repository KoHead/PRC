# -*- coding: utf-8 -*-
"""All the functions for manage the MX values, called by main.py
.. moduleauthor:: Damien Mathieu <damien.mathieu@adthink-media.com>

"""

import os
import sys
import select
import paramiko


def ssh_connection(hostname, username):
    """Established the ssh connexion to he host
    Args:
       hostname (str):  The hostname to use.
       username (str):  The current username.
    Returns:
        int. The return error code::
        1 --  Connection Failure or the username are not the rights to connect to the hostname
    ssh. Paramiko instance connection
    """

    #We testing if the username can to connect to the hostname
    if username == "company1":
        if hostname in open("./servers_list_company1.txt", "r").read():
            pass
        else:
            return 1
    elif username == "company2":
        if hostname in open("./servers_list_company2.txt", "r").read():
            pass
        else:
            return 1
    else:
        return 1

    #Connexion au serveur (nb, il faut que l'échange de clé ssh est eu lieu)
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username="postfix", timeout=4)
        print "Connected to %s" % hostname
    except paramiko.AuthenticationException:
        return 1
    except:
        return 1

    return ssh

def return_listserver(username):
    """Return server list of servers connected to api. (server available)
       Returns:
        list. : Server list available (from servers_list.txt)
       Raises:
        str. : Error message
    """
    if username == "company1":
        # Ouverture du fichier source
        source = open("/home/adthink_mx_api/FlaskApp/servers_list_company1.txt", "r").read().splitlines()
        return source
        source.close()
    elif username == "company2":
        source = open("/home/adthink_mx_api/FlaskApp/servers_list_company2.txt", "r").read().splitlines()
        return source
        source.close()
    else:
        source = "You are not the rights"
        return source



def return_domain_deleted(hostname,domain_name, username):
    """Delete a domain (and all the MX values in main.cf and master.cf)
       Args:
        hostname (str) : The hostname
        domain_namn (str) : The domain name
       Returns:
        str. : Succes message or error message.
    """
    myconnection = ssh_connection(hostname, username)
    if myconnection == 1:
        return "Connection to %s failed" % hostname
    else:
        #On test si le domaine existe bien sur le serveur
        commandline="sudo /usr/sbin/postconf  -P */unix/syslog_name | cut -d '/' -f 1 | grep %s " % domain_name
        stdin, stdout, stderr = myconnection.exec_command(commandline)
    if not stdout.read():
        #Le domaine n'existe pas, on stoppe
        return "The domain does not exist"
        exit(1)
    else:
        list = []
        #Les commandes a envoyer
        #Suppression main.cf
        commandline="sudo /usr/sbin/postconf -X %s_destination_concurrency_limit" % domain_name
        list.append(commandline)
        commandline="sudo /usr/sbin/postconf -X %s_destination_rate_delay" % domain_name
        list.append(commandline)
        commandline="sudo /usr/sbin/postconf -X %s_destination_recipient_limit" % domain_name
        list.append(commandline)
        commandline="sudo /usr/sbin/postconf -X %s_initial_destination_concurrency" % domain_name
        list.append(commandline)
        #Suppression master.cf
        commandline="sudo /usr/sbin/postconf -XM %s/unix" % domain_name
        list.append(commandline)

        #On effectue chaque commande
        for i in list:
           stdin, stdout, stderr = myconnection.exec_command(i)
           #Si une erreur est retournée
           if stderr.read():
               is_deleted=False
           else:
               is_deleted=True

        if is_deleted == True:
            #Reload conf postfix
            stdin, stdout, stderr = myconnection.exec_command("sudo /etc/init.d/postfix reload")
            if stderr.read():
                return "The domain has not been deleted. Failed. The server postfix has not restarted. Please contact system administrator "
            else:
                return "The domain %s has been deleted" % domain_name
        else:
           return "The domain has not been deleted. Failed, please contact system administrator "

    # Disconnect from the host
    myconnection.close()


def return_domain_values(hostname, domain_name, username):
    """Return MX values for a domain from a hostname
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
    myconnection = ssh_connection(hostname, username)
    if myconnection == 1:
        return "Connection to %s failed" % hostname
    else:
        #If the user want the defaults values
        if domain_name == "default":
            list = []
            #Get the default destination
            stdin, stdout, stderr = myconnection.exec_command("/bin/cat /etc/postfix/main.cf | grep default_destination | cut -d '=' -f 2" )
            out=stdout.read().splitlines()
        else:
            # Send the command (non-blocking)
            commandline="/bin/cat /etc/postfix/main.cf | grep %s | cut -d '=' -f 2" % (domain_name)
            stdin, stdout, stderr = myconnection.exec_command(commandline)

            #On récupère la sortie standard
            out=stdout.read().splitlines()

    if not out:
        # Disconnect from the host
        myconnection.close()
        return "No value for this domain. Are you sure this domain exist ?"
        exit(1)
    else:
        # Disconnect from the host
        myconnection.close()
        #On retourne la liste des domaines
        return out


def return_domains(hostname, username):
    """Return a list of domains for a hostname (in args)
      Args:
        hostname (str) : The hostname
      Returns:
        list. : Domains list
       Raises:
        str. : Error message
    """
    myconnection = ssh_connection(hostname, username)
    if myconnection == 1:
        return "Connection to %s failed" % hostname
    else:
       # Send the command (non-blocking)
        stdin, stdout, stderr = myconnection.exec_command("sudo /usr/sbin/postconf  -P */unix/syslog_name | cut -d '/' -f 1")

        #On récupère la sortie standard
        out=stdout.read().splitlines()

        if not out:
            return "No domains for this hostname"
        else:
            #On retourne la liste des domaines
            return out
    # Disconnect from the host
    myconnection.close()

def return_domain_added(hostname, domain_name, value1, value2, value3, username):
    """ Add a domain (if does not exist) and the MX values
        Args:
         hostname (str) : The hostname
         domain_name (str) : The domain name
         value1 (int) : destination_concurrency_limit (ex: 60)
         value2 (int) : destination_recipient_limit (ex: 20)
         value3 (int) : destination_rate_delay (in second) (ex: 1)
        Returns:
         str. : Succes message or error message (domain already exist)
    """
    #Established the connection
    myconnection = ssh_connection(hostname, username)
    if myconnection == 1:
        return "Connection to %s failed" % hostname
    else:
        if domain_name == "default":
            #We will to test if the domain already exist in the postfix configuration
            commandline="sudo /usr/sbin/postconf  -P */unix/syslog_name | cut -d '/' -f 1 | grep default_destination"
            stdin, stdout, stderr = myconnection.exec_command(commandline)
            if stdout.read():
                #The domain does not exist, exit
                return "This domain already exist"
            else:
                list = []
                #Command to send to the host
                commandline="sudo /usr/sbin/postconf -e default_destination_concurrency_limit=%d" % value1
                #We added the commanline(s) to a list.
                #Paramiko can only send one command at a time
                list.append(commandline)
                #Next command
                commandline="sudo /usr/sbin/postconf -e default_destination_recipient_limit=%d" % value2
                list.append(commandline)
                commandline="sudo /usr/sbin/postconf -e default_destination_rate_delay=%ds" % value3
                list.append(commandline)
                #We send the commands
                for i in list:
                    stdin, stdout, stderr = myconnection.exec_command(i)
                    #if error
                    if stderr.read():
                        is_added=False
                    else:
                        is_added=True

                if is_added == True:
                    #Reload conf postfix
                    stdin, stdout, stderr = myconnection.exec_command("sudo /etc/init.d/postfix reload")
                    if stderr.read():
                        return "The domain has not been added. Failed. The server postfix has not restarted. Please contact system administrator "
                    else:
                        return "The domain %s has been added" % domain_name
                else:
                    return "The domain has not been added. Failed, please contact system administrator "

        else:
            #We will to test if the domain already exist in the postfix configuration
            commandline="sudo /usr/sbin/postconf  -P */unix/syslog_name | cut -d '/' -f 1 | grep %s " % domain_name
            stdin, stdout, stderr = myconnection.exec_command(commandline)
            if stdout.read():
                #The domain does not exist, exit
                return "This domain already exist"
            else:
                list = []
                #Command to send to the host
                commandline="sudo /usr/sbin/postconf -e %s_destination_concurrency_limit=%d" % (domain_name, value1)
                #We added the commanline(s) to a list.
                #Paramiko can only send one command at a time
                list.append(commandline)
                #Next command
                commandline="sudo /usr/sbin/postconf -e %s_destination_recipient_limit=%d" % (domain_name, value2)
                list.append(commandline)
                commandline="sudo /usr/sbin/postconf -e %s_destination_rate_delay=%ds" % (domain_name, value3)
                list.append(commandline)
                commandline=commandline="sudo /usr/sbin/postconf -M %s/unix/=\"%s      unix  -       -       n       -       -       smtp -o syslog_name=postfix-%s\"" % (domain_name, domain_name, domain_name)
                list.append(commandline)

                #We send the commands
                for i in list:
                    stdin, stdout, stderr = myconnection.exec_command(i)
                    #if error
                    if stderr.read():
                        is_added=False
                    else:
                        is_added=True

                if is_added == True:
                    #Reload conf postfix
                    stdin, stdout, stderr = myconnection.exec_command("sudo /etc/init.d/postfix reload")
                    if stderr.read():
                        return "The domain has not been added. Failed. The server postfix has not restarted. Please contact system administrator "
                    else:
                        return "The domain %s has been added" % domain_name
                else:
                    return "The domain has not been added. Failed, please contact system administrator "

    # Disconnect from the host
    myconnection.close()

def return_domain_updated(hostname, domain_name, value1, value2, value3, username):
    """ Add a domain (if does not exist) and the MX values
    Args:
    hostname (str) : The hostname
    domain_name (str) : The domain name
    value1 (int) : destination_concurrency_limit (ex: 60)
    value2 (int) : destination_recipient_limit (ex: 20)
    value3 (int) : destination_rate_delay (in second) (ex: 1)
    Returns:
    str. : Succes message or error message (domain already exist)
    """
    #Established the connection
    myconnection = ssh_connection(hostname, username)
    if myconnection == 1:
        return "Connection to %s failed" % hostname
    else:
        if domain_name == "default":
            #We will to test if the domain already exist in the postfix configuration
            commandline="sudo /usr/sbin/postconf  -P */unix/syslog_name | cut -d '/' -f 1 | grep default_destination  "
            stdin, stdout, stderr = myconnection.exec_command(commandline)
            if stdout.read():
                #The domain does not exist, exit
                return "This domain already exist"
            else:
                list = []
                #Command to send to the host
                commandline="sudo /usr/sbin/postconf -e default_destination_concurrency_limit=%d" % value1
                #We added the commanline(s) to a list.
                #Paramiko can only send one command at a time
                list.append(commandline)
                #Next command
                commandline="sudo /usr/sbin/postconf -e default_destination_recipient_limit=%d" % value2
                list.append(commandline)
                commandline="sudo /usr/sbin/postconf -e default_destination_rate_delay=%ds" % value3
                list.append(commandline)

            #We send the commands
            for i in list:
                stdin, stdout, stderr = myconnection.exec_command(i)
                #if error
                if stderr.read():
                    is_added=False
                else:
                    is_added=True

            if is_added == True:
               #Reload conf postfix
               stdin, stdout, stderr = myconnection.exec_command("sudo /etc/init.d/postfix reload")
               if stderr.read():
                   return "The domain has not been updated. Failed. The server postfix has not restarted. Please contact system administrator "
               else:
                   return "The domain %s has been updated" % domain_name
            else:
               return "The domain has not been updated. Failed, please contact system administrator "

        else:
            #We will to test if the domain already exist in the postfix configuration
            commandline="sudo /usr/sbin/postconf  -P */unix/syslog_name | cut -d '/' -f 1 | grep %s " % domain_name
            stdin, stdout, stderr = myconnection.exec_command(commandline)
            if not stdout.read():
                #The domain does not exist, exit
                return "This domain does not exist, you can't update it"
            else:
                list = []
                #Command to send to the host
                commandline="sudo /usr/sbin/postconf -e %s_destination_concurrency_limit=%s" % (domain_name, value1)
                #We added the commanline(s) to a list.
                #Paramiko can only send one command at a time
                list.append(commandline)
                #Next command
                commandline="sudo /usr/sbin/postconf -e %s_destination_recipient_limit=%s" % (domain_name, value2)
                list.append(commandline)
                commandline="sudo /usr/sbin/postconf -e %s_destination_rate_delay=%ss" % (domain_name, value3)
                list.append(commandline)

                #We send the commands
                for i in list:
                    stdin, stdout, stderr = myconnection.exec_command(i)
                    #if error
                    if stderr.read():
                        is_added=False
                    else:
                        is_added=True

                if is_added == True:
                    #Reload conf postfix
                    stdin, stdout, stderr = myconnection.exec_command("sudo /etc/init.d/postfix reload")
                    if stderr.read():
                        return "The domain has not been updated. Failed. The server postfix has not restarted. Please contact system administrator "
                    else:
                        return "The domain %s has been updated" % domain_name
                else:
                    return "The domain has not been updated. Failed, please contact system administrator "

    # Disconnect from the host
    myconnection.close()


def return_get_transport(hostname, domain_name, username):
    """ Return the list of extensions of domains include in postfix transport file
    Args:
     hostname (str) : The hostname
     domain_name (str) : The domain name
    Returns:
     str. : Succes message or error message (domain does not exist)
    """
    #Established the connection
    myconnection = ssh_connection(hostname, username)
    if myconnection == 1:
        return "Connection to %s failed" % hostname
    else:
        #We will to test if the domain already exist in the postfix configuration
        commandline="/bin/cat /etc/postfix/transport | grep %s | awk '{print $1}'" % domain_name
        stdin, stdout, stderr = myconnection.exec_command(commandline)
        #We getting the stdout
        out=stdout.read().splitlines()

        if not out:
            return "No values for this domain. Are you sure this domain exist ?"
            exit(1)
        else:
            # Disconnect from the host
            myconnection.close()
            #We return to flask app the value (a python list)
            return out



def return_add_transport(hostname, domain_name, domain_extension, username):
    """ Add a domain extension (if does not exist) for a domain name in transport file
    Args:
     hostname (str) : The hostname
     domain_name (str) : The domain name (not fqdn)
     domain_extension (str) : The domain name with the extension (fqdn)
    Returns:
     str. : Succes message or error message (domain extension already exist)
    """
    #Established the connection
    myconnection = ssh_connection(hostname, username)
    if myconnection == 1:
        return "Connection to %s failed" % hostname
    else:
        #We will to test if the domain already exist in the postfix configuration
        commandline="/bin/cat /etc/postfix/transport | grep %s | awk '{print $1}' | grep %s" % (domain_name, domain_extension)
        print commandline
        stdin, stdout, stderr = myconnection.exec_command(commandline)
        if stdout.read():
            #The domain does not exist, exit
            return "This domain extension (%s) already exist for the domain name %s" % (domain_extension, domain_name)
        else:
            #Command to send to the host
            commandline="echo \"%s           %s:\" >> /etc/postfix/transport" % (domain_extension, domain_name)
            stdin, stdout, stderr = myconnection.exec_command(commandline)
            if stderr.read():
                is_added=False
            else:
                is_added=True

            if is_added == True:
                stdin, stdout, stderr = myconnection.exec_command("sudo /usr/sbin/postmap /etc/postfix/transport")
                #Reload conf postfix
                stdin, stdout, stderr = myconnection.exec_command("sudo /etc/init.d/postfix restart")
                if stderr.read():
                    return "The domain extension has not been added. Failed. The server postfix has not restarted. Please contact system administrator "
                else:
                    return "This domain extension (%s) has been added for the domain name %s" % (domain_extension, domain_name)
            else:
                    return "The domain extension has not been added. Failed. Please contact system administrator "

    # Disconnect from the host
    myconnection.close()

def return_del_transport(hostname, domain_name, domain_extension, username):
    """ Delete a domain extension (if exist) for a domain name in transport file
    Args:
     hostname (str) : The hostname
     domain_name (str) : The domain name (not fqdn)
     domain_extension (str) : The domain name with the extension (fqdn)
    Returns:
     str. : Succes message or error message (domain extension does not exist)
    """
    #Established the connection
    myconnection = ssh_connection(hostname, username)
    if myconnection == 1:
        return "Connection to %s failed" % hostname
    else:
        #We will to test if the domain already exist in the postfix configuration
        commandline="/bin/cat /etc/postfix/transport | grep %s | awk '{print $1}' | grep %s" % (domain_name, domain_extension)
        stdin, stdout, stderr = myconnection.exec_command(commandline)
        if not stdout.read():
            #The domain does not exist, exit
            return "This domain extension (%s) does not exist for the domain name %s. Not deleted" % (domain_extension, domain_name)
        else:
            #Command to send to the host
            commandline="sudo sed -i '/%s/d' /etc/postfix/transport" % (domain_extension)
            print commandline
            stdin, stdout, stderr = myconnection.exec_command(commandline)
            if stderr.read():
                is_added=False
            else:
                is_added=True

            if is_added == True:
                stdin, stdout, stderr = myconnection.exec_command("sudo /usr/sbin/postmap /etc/postfix/transport")
                #Reload conf postfix
                stdin, stdout, stderr = myconnection.exec_command("sudo /etc/init.d/postfix restart")
                if stderr.read():
                    return "The domain extension has not been deleted. Failed. The server postfix has not restarted. Please contact system administrator "
                else:
                    return "This domain extension (%s) has been deleted for the domain name %s" % (domain_extension, domain_name)
            else:
                return "The domain extension has not been deleted. Failed. Please contact system administrator "

    # Disconnect from the host
    myconnection.close()

 def return_del_queue(hostname, username):
     """Delete the postfix queue
     Args:
      hostname (str): The hostname
     """
     #Established the connection
     myconnection = ssh_connection(hostname, username)
     if myconnection == 1:
         return "Connection to %s failed" % hostname
     else:
         #Empty the queue
         commandline="sudo /usr/sbin/postsuper -d ALL"
         stdin, stdout, stderr = myconnection.exec_command(commandline)
         if stderr.read():
             return "Problem with the queue. Not flushed. Please contact system administrator (admin@adthink-media.com)!"
         else:
             return "The postfix queue on (%s) has been flushed" % (hostname)

     # Disconnect from the host
     myconnection.close()
