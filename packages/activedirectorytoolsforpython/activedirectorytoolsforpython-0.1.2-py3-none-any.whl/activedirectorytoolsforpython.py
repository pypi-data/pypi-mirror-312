"""
Author: Jess Williams
Email: devel@inuxnet.org
Date: 11-28-2024
Desc: Library of classes and functions for common functions
      for interfacing with Microsoft Active Directory. These
      functions are designed to be intuitive for those familiar
      with the Powershell Active Directory module. This 
      library will be complimented with powershell modules for
      Linux to provide similar AD Functions in a Linux 
      Environment.
"""
from ldap3 import Server, Connection, Tls, ALL, ALL_ATTRIBUTES, SUBTREE
import ldap3
import ssl
import getpass
import os
import traceback
import sys
import argparse
import json
import gssapi
from datetime import datetime
import base64
from inuxnetutil import validate_argument, is_empty_string

# Globals - Can set Environment Variables for the following to alter these defaults
global KRB5_CONF, AD_PAGE_SIZE, AD_CONNECT_TIMEOUT, INDENT_SPACES
KRB5_CONF = os.environ.get("KRB5_CONF", "/etc/krb5.conf")
AD_PAGE_SIZE = os.environ.get("AD_PAGE_SIZE", 300000)
AD_CONNECT_TIMEOUT = os.environ.get("AD_CONNECT_TIMEOUT", 2)
INDENT_SPACES = os.environ.get("INDENT_SPACES", 4)


class ADObject:
    """
    Top Level AD Object. Attributes are dynamically set based on output of LDAP query.
    """
    def __init__(self, data_dict: dict):
        """
        Constructor
        :param data_dict: <class 'dict'>
            - The raw data output from LDAP query
        """
        data_dict = validate_argument(data_dict, dict, "data_dict")
        for key, value in data_dict.items():
            name = key.replace('.', '_')
            if len(value) == 1:
                setattr(self, name, value[0])
            else:
                setattr(self, name, value)

    def get_json(self):
        """
        Returns JSON formatted String
        :return: <class 'str'>
        """
        def custom_serializer(obj):
            if isinstance(obj, datetime):
                return str(obj)
            elif isinstance(obj, bytes):
                return base64.b64encode(obj).decode('utf-8')
            raise TypeError(f"Type {type(obj)} not serializable")

        return json.dumps(self.__dict__, default=custom_serializer)

    def __str__(self):
        """
        String override
        :return: <class 'str'>
            - Formatted string representation of AD Object
        """
        global INDENT_SPACES
        output = f"DN: {self.distinguishedName}:\n"
        output += f"Category: {self.objectCategory}\n"
        spaces = " " * INDENT_SPACES
        for k,v in self.__dict__.items():
            output += f"{spaces}{k}: "
            if not isinstance(v, list):
                if isinstance(v, bytes):
                    output += f"{base64.b64encode(v).decode('utf-8')}\n"
                else:
                    output += f"{v}\n"
            else:
                output += "\n"
                for item in v:
                    output += f"{spaces*2}{item}\n"
        return output


class ADUser(ADObject):
    """
    AD User Object.
    """
    def __init__(self, data_dict: dict):
        """
        Constructor
        :param data_dict: <class 'dict'>
            - The raw data output from LDAP query
        """
        super().__init__(data_dict)


class ADGroup(ADObject):
    """
    AD Group Object.
    """
    def __init__(self, data_dict: dict):
        """
        Constructor
        :param data_dict: <class 'dict'>
            - The raw data output from LDAP query
        """
        super().__init__(data_dict)


class ADComputer(ADObject):
    """
    AD Computer Object.
    """
    def __init__(self, data_dict: dict):
        """
        Constructor
        :param data_dict: <class 'dict'>
            - The raw data output from LDAP query
        """
        super().__init__(data_dict)


class ADOrganizationalUnit(ADObject):
    """
    AD OrganizationalUnit Object.
    """
    def __init__(self, data_dict: dict):
        """
        Constructor
        :param data_dict: <class 'dict'>
            - The raw data output from LDAP query
        """
        super().__init__(data_dict)


class Realm:
    """
    Kerberos Config Realm Object
    """
    def __init__(self, data_dict: dict):
        """
        Constructor
        :param data_dict: <class 'dict'>
            - The raw data output from Kerberos Config
        """
        data_dict = validate_argument(data_dict, dict, "data_dict")
        for key, value in data_dict.items():
            name = key.replace('.', '_')
            # Add the property to the class
            setattr(self, name, value)


class Realms:
    """
    Kerberos Config Realms Object, contains realm objects
    """
    def __init__(self, data_dict: dict):
        """
        Constructor
        :param data_dict: <class 'dict'>
            - The raw data output from Kerberos Config
        """
        data_dict = validate_argument(data_dict, dict, "data_dict")
        for key, value in data_dict.items():
            name = key.replace('.', '_')
            # Add the property to the class
            setattr(self, name, Realm(value))


class LibDefaults:
    """
    Kerberos Config LibDefaults Object
    """
    def __init__(self, data_dict: dict):
        """
        Constructor
        :param data_dict: <class 'dict'>
            - The raw data output from Kerberos Config
        """
        data_dict = validate_argument(data_dict, dict, "data_dict")
        for key, value in data_dict.items():
            name = key.replace('.', '_')
            # Add the property to the class
            setattr(self, name, value)


class DomainRealm:
    """
    Kerberos Domain Realm Object
    """
    def __init__(self, data_dict: dict):
        """
        Constructor
        :param data_dict: <class 'dict'>
            - The raw data output from Kerberos Config
        """
        data_dict = validate_argument(data_dict, dict, "data_dict")
        for key, value in data_dict.items():
            name = key.replace('.', '_')
            # Add the property to the class
            setattr(self, name, value)


class KerberosConfig:
    """
    Top Level Kerberos Config Object (HasA Relationship)
    """
    def __init__(self, config_path: str = None):
        """
        Constructor
        :param config_path: <class 'str'>
            - Path to Kerberos Config. Can use global if ommitted.
        """
        krb5 = load_krb5_config(config_path)
        if krb5 is not None:
            for key, value in krb5.items():
                name = key.replace('.', '_')
                # Store the value in the instance dictionary
                if key == "libdefaults":
                    setattr(self, name, LibDefaults(value))
                elif key == "realms":
                    setattr(self, name, Realms(value))
                elif key == "domain_realm":
                    setattr(self, name, DomainRealm(value))
                else:
                    setattr(self, name, value)


def load_krb5_config(config_path: str = None):
    """
    Returns a Dictionary of the krb5.conf file.
    :param config_path: <class 'str'>
        -  Path to Kerberos Config File. Defaults to Global
    """
    def populate_array(kv: list, open_tag: str, nested_tag: str):
        """
        Nested Recursive Function to populate array/dictionary
        :param kv: <class 'list'>
            - List representing a key[0] value[1] pair
        :param open_tag: <class 'str'>
            - Tag representing the top level key
        :param nested_tag: <class 'str'>
            - Nested key
        """
        if open_tag is not None:
            if nested_tag is not None:
                if nested_tag not in output[open_tag].keys():
                    output[open_tag][nested_tag] = {}
                output[open_tag][nested_tag][kv[0]] = kv[1:] if len(kv) > 2 else kv[1]
            else:
                output[open_tag][kv[0]] = kv[1:] if len(kv) > 2 else kv[1]
        else:
            if nested_tag is not None:
                if nested_tag not in output.keys():
                    output[nested_tag] = {}
                output[nested_tag][kv[0]] = kv[1:] if len(kv) > 2 else kv[1]
            else:
                output[kv[0]] = kv[1:] if len(kv) > 2 else kv[1]

    global KRB5_CONF
    config_path = KRB5_CONF if config_path is None else config_path
    with open(config_path) as f:
        lines = [line.strip() for line in f.readlines() if line.strip() != '']
    output = {}
    open_tag = None
    nested_tag = None
    for line in lines:
        if line.lstrip()[0] != "#":
            if line.find("[") == 0:
                open_tag = line.lstrip("[").rstrip("]")
                output[open_tag] = {}
            else:
                kv = [x.strip() for x in line.split('=')]
                if len(kv) >= 2:
                    if nested_tag is None and kv[1].find("{") == 0:
                        nested_tag = kv[0]
                        continue
                    elif nested_tag is not None and kv[1].find("}") == 0:
                        print("Here")
                        nested_tag = None
                        continue
                    populate_array(kv, open_tag, nested_tag)
                else:
                    if nested_tag is not None and kv[0].find("}") == 0:
                        nested_tag = None
                        continue

    return None if len(output) == 0 else output


def get_default_searchdomain(krb5: KerberosConfig, server: str) -> str:
    """
    Gets default searchdomain based on kerberos config and server values.
    :param krb5: <class 'KerberosConfig'>
        - Object of kerberos config file
    :param server: <class 'str'>
        - Server value
    :return: <class 'str'>
        - The Distinguished name of the search domain
    """
    validate_argument(krb5, KerberosConfig, "krb5")
    validate_argument(server, str, "server")
    if hasattr(krb5, "domain_realm"):
        domains = [x.replace('_','.').lstrip('.') for x in dir(krb5.domain_realm) if x.find('__') != 0]
        matches = {}
        for domain in domains:
            match = server.find(domain.lstrip('.'))
            if match >= 0:
                matches[domain] = match
        best_match = None
        for match in matches.keys():
            value = matches[match]
            if best_match is None or value < best_match[0]:
                best_match = [value, match]
        if best_match is not None:
            output = ""
            for token in match.lstrip('.').split('.'):
                output += f"dc={token},"
            return output.rstrip(',')

    raise ValueError("ERROR: Unable to determine default searchbase, must provide a 'searchbase'.")


def get_default_realm(krb5: KerberosConfig) -> str:
    """
    Gets default realm based on kerberos config.
    :param krb5: <class 'KerberosConfig'>
        - Object of kerberos config file
    :return: <class 'str'>
    """
    validate_argument(krb5, KerberosConfig, "krb5")
    if hasattr(krb5, "libdefaults"):
        if hasattr(krb5.libdefaults, "default_realm"):
            return krb5.libdefaults.default_realm

    raise ValueError("ERROR: Unable to determine default_realm, must provide a 'searchbase' and/or 'server'.")


def get_default_server(krb5: KerberosConfig) -> str:
    """
    Gets default server based on kerberos config.
    :param krb5: <class 'KerberosConfig'>
        - Object of kerberos config file
    :return: <class 'str'>
        - The fqdn of the default realm kdc server.
    """
    validate_argument(krb5, KerberosConfig, "krb5")
    default_realm = get_default_realm(krb5)
    if default_realm is not None:
        if hasattr(krb5, "realms"):
            realm = default_realm.replace('.','_')
            if hasattr(krb5.realms, realm):
                attrib = getattr(krb5.realms, realm)
                if hasattr(attrib, "kdc"):
                    return attrib.kdc.split(':')[0]
                else:
                    raise ValueError(
                        f"ERROR: Unable to locate kdc from realm {default_realm}, must provide a 'server'.")
            else:
                raise ValueError(f"ERROR: Unable to locate {default_realm} from realms, must provide a 'server'.")
        else:
            raise ValueError("ERROR: Unable to determine default server from realms, must provide a 'server'.")
    else:
        raise ValueError("ERROR: Unable to determine default realm, must provide a 'server'.")


def get_adobject(filter: str, server: str = None, searchbase: str = None, cacert: str = None,
                 port: int = 636, tls: bool = True, username: str = None, password: str = None,
                 properties: list = None, verify: bool = True) -> list:
    """
    Gets AD Object.
    :param filter: <class 'str'>
        - The specific ldap filter to query. This parameter is required.
          i.e. (&(objectClass=user)(sAMAccountName=username)) for a specific user
          i.e. (&(objectClass=group)(sAMAccountName=groupname)) for a specific group
          i.e. (&(objectClass=computer)(cn=$($Identity))) for a specific computer
          i.e.  (&(objectClass=organizationalUnit)(ou=$($Identity))) for an ou
    :param server: <class 'str'>
        - The Active Directory Domain Controller to Query
          If None, will Default to the Default Domain server in the krb5.conf.
          If no krb5.conf is available than argument is required.
    :param searchbase: <class 'str'>
        - LDAP Base search path
          If None, will default to the associated root search base from the server
          located in the krb5.conf. If no krb5.conf is available than argument is required.
          i.e. DC=example,DC=com
    :param cacert: <class 'str'>
        - Root CA Certificate Path
          Required if tls=True and verify=True
    :param port: <class 'int'>
        - Port for ldap. Default 636
    :param tls: <class 'bool'>
        - Determines if connectivity should use TLS 1.2. Defaults to True
    :param username: <class 'str'>
        - FQDN of user to authenticate when not using Kerberos. Defaults to None.
    :param password: <class 'str'>
        - Password for user when not using Kerberos. If None will use getpass.
    :param properties: <class 'list'> or <class 'tuple'> or <class 'str'>
        - List of Properties to retrieve. If None will get distinguishedName and
          objectCategory only.
          i.e. properties=["ALL"] # For All Properties
          i.e. properties=["mail","cn"]
    :param verify: <class 'bool'>
        - Verifies the certificate of the server. Defaults to True.
    :return: <class 'list'> or None
        - Returns a list of dictionary objects representing each result.
    """
    objects = get_adobject_raw(filter, server, searchbase, cacert, port, tls, username,
                               password, properties, verify)
    output = []

    if objects is not None:
        ad_objects = []
        for obj in objects:
            ad_objects.append(ADObject(obj))
        return ad_objects

    return None if len(output) == 0 else output


def get_adobject_raw(filter: str, server: str = None, searchbase: str = None, cacert: str = None,
                 port: int = 636, tls: bool = True, username: str = None, password: str = None,
                 properties: list = None, verify: bool = True) -> list:
    """
    Gets AD Object.
    :param filter: <class 'str'>
        - The specific ldap filter to query. This parameter is required. 
          i.e. (&(objectClass=user)(sAMAccountName=username)) for a specific user
          i.e. (&(objectClass=group)(sAMAccountName=groupname)) for a specific group
          i.e. (&(objectClass=computer)(cn=$($Identity))) for a specific computer
          i.e.  (&(objectClass=organizationalUnit)(ou=$($Identity))) for an ou
    :param server: <class 'str'>
        - The Active Directory Domain Controller to Query
          If None, will Default to the Default Domain server in the krb5.conf.
          If no krb5.conf is available than argument is required.
    :param searchbase: <class 'str'>
        - LDAP Base search path
          If None, will default to the associated root search base from the server
          located in the krb5.conf. If no krb5.conf is available than argument is required.
          i.e. DC=example,DC=com
    :param cacert: <class 'str'>
        - Root CA Certificate Path
          Required if tls=True and verify=True
    :param port: <class 'int'>
        - Port for ldap. Default 636
    :param tls: <class 'bool'>
        - Determines if connectivity should use TLS 1.2. Defaults to True
    :param username: <class 'str'>
        - FQDN of user to authenticate when not using Kerberos. Defaults to None.
    :param password: <class 'str'>
        - Password for user when not using Kerberos. If None will use getpass.
    :param properties: <class 'list'> or <class 'tuple'> or <class 'str'>
        - List of Properties to retrieve. If None will get distinguishedName and 
          objectCategory only.
          i.e. properties=["ALL"] # For All Properties
          i.e. properties=["mail","cn"]
    :param verify: <class 'bool'>
        - Verifies the certificate of the server. Defaults to True.
    :return: <class 'list'> or None
        - Returns a list of dictionary objects representing each result.
    """
    def validate_args():
        """
        Validate arguments
        """
        is_empty_string(filter, "filter")
        is_empty_string(server, "server", True)
        is_empty_string(searchbase, "searchbase", True)
        is_empty_string(cacert, "cacert", True)
        validate_argument(port, int, "port", True)
        validate_argument(tls, bool, "tls")
        is_empty_string(username, "username", True)
        is_empty_string(password, "password", True)
        validate_argument(properties, [list, tuple, str], "properties", True)
        validate_argument(verify, bool, "verify")

    # Start of Function/End of nested functions
    global AD_PAGE_SIZE, AD_CONNECT_TIMEOUT
    output = []

    try:
        validate_args()
        krb5 = KerberosConfig()

        # Validate/Get server
        if server is None and krb5 is not None:
            server = get_default_server(krb5)
        elif server is None:
            raise ValueError("ERROR: krb5 failed to load and 'server' parameter cannot be None.")

        # Validate/Set searchbase
        if searchbase is None and krb5 is not None:
            searchbase = get_default_searchdomain(krb5, server)
        elif searchbase is None:
            raise ValueError("ERROR: krb5 failed to load and 'searchbase' parameter cannot be None.")

        # Validate cacert
        if tls:
            if cacert is not None and verify:
                if not os.path.isfile(cacert):
                    raise ValueError(f"ERROR: cacert '{cacert}' path is invalid or cannot be read.")
            elif verify:
                raise ValueError("ERROR: connection set to TLS with tls=True, must provide a cacert path.")

        # Validate username/password
        if username is not None:
            if password is None:
                password = getpass.getpass(f"Enter passphrase for '{username}': ")

        if tls:
            validate = ssl.CERT_REQUIRED if verify else ssl.CERT_NONE
            LDAP_SERVER = f"ldaps://{server}"
            tls_configuration = Tls(
                validate=validate,
                version=ssl.PROTOCOL_TLSv1_2,  # Use TLS 1.2
                ca_certs_file=cacert  # Path to CA certificate
            )
        else:
            LDAP_SERVER = f"ldap://{server}"
            tls_configuration = None

        ldap = Server(
            LDAP_SERVER,
            port,
            use_ssl=ssl,
            tls=tls_configuration,
            connect_timeout=AD_CONNECT_TIMEOUT,
            get_info=ALL
        )

        if username is not None:  # Connect using username and password
            conn = Connection(
                ldap,
                user=username,
                password=password,
                authentication='SIMPLE',
                auto_bind=True
            )
        else:  # Connect using SASL/GSSAPI (Kerberos)
            conn = Connection(
                ldap,
                authentication='SASL',
                sasl_mechanism='GSSAPI',
                auto_bind=True
            )

        if properties is not None:
            if not isinstance(properties, list) and not isinstance(properties, tuple):
                properties = [properties]
            normalize_properties = [prop.lower() for prop in properties if prop.strip() != '']
            if 'all' in normalize_properties or '*' in properties:
                attributes = ALL_ATTRIBUTES
            else:
                attributes = [prop for prop in properties if prop.strip() != '']
                if "distinguishedname" not in normalize_properties:
                    attributes.append("distinguishedName")
                    attributes.append("objectCategory")
        else:
            attributes = ['distinguishedName', 'objectCategory']

        conn.search(
            search_base=searchbase,
            search_filter=filter,
            attributes=attributes,
            paged_size=AD_PAGE_SIZE,
            search_scope=SUBTREE
        )

        results = [{key: entry.entry_attributes_as_dict[key]
                    for key in sorted(entry.entry_attributes_as_dict)}
                   for entry in conn.entries]

        # Unbind the connection
        conn.unbind()

        return results

    except ValueError as e:
        print(e, file=sys.stderr)
    except TypeError as e:
        print(e, file=sys.stderr)
    except ldap3.core.exceptions.LDAPAttributeError as e:
        print(f"ERROR - Invalid Property(s) or Filter: {e}", file=sys.stderr)
    except ldap3.core.exceptions.LDAPBindError as e:
        print(f"ERROR - Bind Error: {e}", file=sys.stderr)
    except ldap3.core.exceptions.LDAPSocketOpenError as e:
        print(f"ERROR - The Socket failed to open, check your server or port config: {e}", file=sys.stderr)
    except gssapi.raw.misc.GSSError as e:
        print(f"ERROR - The Kerberos ticket has expired or is not set: {e}", file=sys.stderr)
    except Exception as e:
        print(f"ERROR - An unexpected error occurred: {e}", file=sys.stderr)
        traceback.print_exc()

    return None if len(output) == 0 else output


def get_aduser(filter: str=None, identity: str=None, server: str = None,
                 searchbase: str = None, cacert: str = None, port: int = 636,
                 tls: bool = True, username: str = None, password: str = None,
                 properties: list = None, verify: bool = True) -> list:
    """
    Gets AD User Object(s).
    :param filter: <class 'str'>
        - The specific ldap filter to query. This parameter is required.
          i.e. sn=lastname for a specific user
    :param identity: <class 'str'>
        - Can be a sAMAccountName, DistinguishedName, or userPrincipalName
    :param server: <class 'str'>
        - The Active Directory Domain Controller to Query
          If None, will Default to the Default Domain server in the krb5.conf.
          If no krb5.conf is available than argument is required.
    :param searchbase: <class 'str'>
        - LDAP Base search path
          If None, will default to the associated root search base from the server
          located in the krb5.conf. If no krb5.conf is available than argument is required.
          i.e. DC=example,DC=com
    :param cacert: <class 'str'>
        - Root CA Certificate Path
          Required if tls=True and verify=True
    :param port: <class 'int'>
        - Port for ldap. Default 636
    :param tls: <class 'bool'>
        - Determines if connectivity should use TLS 1.2. Defaults to True
    :param username: <class 'str'>
        - FQDN of user to authenticate when not using Kerberos. Defaults to None.
    :param password: <class 'str'>
        - Password for user when not using Kerberos. If None will use getpass.
    :param properties: <class 'list'> or <class 'tuple'> or <class 'str'>
        - List of Properties to retrieve. If None will get distinguishedName and
          objectCategory only.
          i.e. properties=["ALL"] # For All Properties
          i.e. properties=["mail","cn"]
    :param verify: <class 'bool'>
        - Verifies the certificate of the server. Defaults to True.
    :return: <class 'list'> or None
        - Returns a list of dictionary objects representing each result.
    """
    user_objects_raw = get_aduser_raw(filter, identity, server, searchbase, cacert, port, tls, username, password,
                                      properties, verify)
    users = []
    for user_raw in user_objects_raw:
        users.append(ADUser(user_raw))

    return None if len(users) == 0 else users


def get_aduser_raw(filter: str=None, identity: str=None, server: str = None,
                 searchbase: str = None, cacert: str = None, port: int = 636,
                 tls: bool = True, username: str = None, password: str = None,
                 properties: list = None, verify: bool = True) -> list:
    """
    Gets AD User Object(s) raw data.
    :param filter: <class 'str'>
        - The specific ldap filter to query. This parameter is required.
          i.e. sn=lastname for a specific user
    :param identity: <class 'str'>
        - Can be a sAMAccountName, DistinguishedName, or userPrincipalName
    :param server: <class 'str'>
        - The Active Directory Domain Controller to Query
          If None, will Default to the Default Domain server in the krb5.conf.
          If no krb5.conf is available than argument is required.
    :param searchbase: <class 'str'>
        - LDAP Base search path
          If None, will default to the associated root search base from the server
          located in the krb5.conf. If no krb5.conf is available than argument is required.
          i.e. DC=example,DC=com
    :param cacert: <class 'str'>
        - Root CA Certificate Path
          Required if tls=True and verify=True
    :param port: <class 'int'>
        - Port for ldap. Default 636
    :param tls: <class 'bool'>
        - Determines if connectivity should use TLS 1.2. Defaults to True
    :param username: <class 'str'>
        - FQDN of user to authenticate when not using Kerberos. Defaults to None.
    :param password: <class 'str'>
        - Password for user when not using Kerberos. If None will use getpass.
    :param properties: <class 'list'> or <class 'tuple'> or <class 'str'>
        - List of Properties to retrieve. If None will get distinguishedName and
          objectCategory only.
          i.e. properties=["ALL"] # For All Properties
          i.e. properties=["mail","cn"]
    :param verify: <class 'bool'>
        - Verifies the certificate of the server. Defaults to True.
    :return: <class 'list'> or None
        - Returns a list of dictionary objects representing each result.
    """
    if identity is not None:
        ldap_filter = f"(&(objectClass=user)(|(sAMAccountName={identity})(distinguishedName={identity})(userPrincipalName={identity})))"
    else:
        if filter is not None:
            ldap_filter = f"(&(objectClass=user)({filter}))"
        else:
            ldap_filter = None

    return get_adobject_raw(ldap_filter, server, searchbase, cacert, port, tls, username, password, properties, verify)


def get_adgroup(filter: str=None, identity: str=None, server: str = None,
                 searchbase: str = None, cacert: str = None, port: int = 636,
                 tls: bool = True, username: str = None, password: str = None,
                 properties: list = None, verify: bool = True) -> list:
    """
    Gets AD Group Object(s).
    :param filter: <class 'str'>
        - The specific ldap filter to query. This parameter is required.
    :param identity: <class 'str'>
        - Can be a sAMAccountName, DistinguishedName
    :param server: <class 'str'>
        - The Active Directory Domain Controller to Query
          If None, will Default to the Default Domain server in the krb5.conf.
          If no krb5.conf is available than argument is required.
    :param searchbase: <class 'str'>
        - LDAP Base search path
          If None, will default to the associated root search base from the server
          located in the krb5.conf. If no krb5.conf is available than argument is required.
          i.e. DC=example,DC=com
    :param cacert: <class 'str'>
        - Root CA Certificate Path
          Required if tls=True and verify=True
    :param port: <class 'int'>
        - Port for ldap. Default 636
    :param tls: <class 'bool'>
        - Determines if connectivity should use TLS 1.2. Defaults to True
    :param username: <class 'str'>
        - FQDN of user to authenticate when not using Kerberos. Defaults to None.
    :param password: <class 'str'>
        - Password for user when not using Kerberos. If None will use getpass.
    :param properties: <class 'list'> or <class 'tuple'> or <class 'str'>
        - List of Properties to retrieve. If None will get distinguishedName and
          objectCategory only.
          i.e. properties=["ALL"] # For All Properties
          i.e. properties=["mail","cn"]
    :param verify: <class 'bool'>
        - Verifies the certificate of the server. Defaults to True.
    :return: <class 'list'> or None
        - Returns a list of dictionary objects representing each result.
    """
    group_objects_raw = get_adgroup_raw(filter, identity, server, searchbase, cacert, port, tls, username, password,
                                      properties, verify)
    groups = []
    for group_raw in group_objects_raw:
        groups.append(ADGroup(group_raw))

    return None if len(groups) == 0 else groups


def get_adgroup_raw(filter: str=None, identity: str=None, server: str = None,
                 searchbase: str = None, cacert: str = None, port: int = 636,
                 tls: bool = True, username: str = None, password: str = None,
                 properties: list = None, verify: bool = True) -> list:
    """
    Gets AD Group Object(s) raw data.
    :param filter: <class 'str'>
        - The specific ldap filter to query. This parameter is required.
    :param identity: <class 'str'>
        - Can be a sAMAccountName, DistinguishedName
    :param server: <class 'str'>
        - The Active Directory Domain Controller to Query
          If None, will Default to the Default Domain server in the krb5.conf.
          If no krb5.conf is available than argument is required.
    :param searchbase: <class 'str'>
        - LDAP Base search path
          If None, will default to the associated root search base from the server
          located in the krb5.conf. If no krb5.conf is available than argument is required.
          i.e. DC=example,DC=com
    :param cacert: <class 'str'>
        - Root CA Certificate Path
          Required if tls=True and verify=True
    :param port: <class 'int'>
        - Port for ldap. Default 636
    :param tls: <class 'bool'>
        - Determines if connectivity should use TLS 1.2. Defaults to True
    :param username: <class 'str'>
        - FQDN of user to authenticate when not using Kerberos. Defaults to None.
    :param password: <class 'str'>
        - Password for user when not using Kerberos. If None will use getpass.
    :param properties: <class 'list'> or <class 'tuple'> or <class 'str'>
        - List of Properties to retrieve. If None will get distinguishedName and
          objectCategory only.
          i.e. properties=["ALL"] # For All Properties
          i.e. properties=["mail","cn"]
    :param verify: <class 'bool'>
        - Verifies the certificate of the server. Defaults to True.
    :return: <class 'list'> or None
        - Returns a list of dictionary objects representing each result.
    """
    if identity is not None:
        ldap_filter = f"(&(objectClass=group)(|(sAMAccountName={identity})(distinguishedName={identity})))"
    else:
        if filter is not None:
            ldap_filter = f"(&(objectClass=group)({filter}))"
        else:
            ldap_filter = None

    return get_adobject_raw(ldap_filter, server, searchbase, cacert, port, tls, username, password, properties, verify)


def get_adcomputer(filter: str=None, identity: str=None, server: str = None,
                 searchbase: str = None, cacert: str = None, port: int = 636,
                 tls: bool = True, username: str = None, password: str = None,
                 properties: list = None, verify: bool = True) -> list:
    """
    Gets AD Computer Object(s).
    :param filter: <class 'str'>
        - The specific ldap filter to query. This parameter is required.
    :param identity: <class 'str'>
        - Can be a sAMAccountName, DistinguishedName
    :param server: <class 'str'>
        - The Active Directory Domain Controller to Query
          If None, will Default to the Default Domain server in the krb5.conf.
          If no krb5.conf is available than argument is required.
    :param searchbase: <class 'str'>
        - LDAP Base search path
          If None, will default to the associated root search base from the server
          located in the krb5.conf. If no krb5.conf is available than argument is required.
          i.e. DC=example,DC=com
    :param cacert: <class 'str'>
        - Root CA Certificate Path
          Required if tls=True and verify=True
    :param port: <class 'int'>
        - Port for ldap. Default 636
    :param tls: <class 'bool'>
        - Determines if connectivity should use TLS 1.2. Defaults to True
    :param username: <class 'str'>
        - FQDN of user to authenticate when not using Kerberos. Defaults to None.
    :param password: <class 'str'>
        - Password for user when not using Kerberos. If None will use getpass.
    :param properties: <class 'list'> or <class 'tuple'> or <class 'str'>
        - List of Properties to retrieve. If None will get distinguishedName and
          objectCategory only.
          i.e. properties=["ALL"] # For All Properties
          i.e. properties=["mail","cn"]
    :param verify: <class 'bool'>
        - Verifies the certificate of the server. Defaults to True.
    :return: <class 'list'> or None
        - Returns a list of dictionary objects representing each result.
    """
    computer_objects_raw = get_adcomputer_raw(filter, identity, server, searchbase, cacert, port, tls, username, password,
                                      properties, verify)
    computers = []
    for computer_raw in computer_objects_raw:
        computers.append(ADComputer(computer_raw))

    return None if len(computers) == 0 else computers


def get_adcomputer_raw(filter: str=None, identity: str=None, server: str = None,
                 searchbase: str = None, cacert: str = None, port: int = 636,
                 tls: bool = True, username: str = None, password: str = None,
                 properties: list = None, verify: bool = True) -> list:
    """
    Gets AD Computer Object(s) raw data.
    :param filter: <class 'str'>
        - The specific ldap filter to query. This parameter is required.
    :param identity: <class 'str'>
        - Can be a sAMAccountName, DistinguishedName
    :param server: <class 'str'>
        - The Active Directory Domain Controller to Query
          If None, will Default to the Default Domain server in the krb5.conf.
          If no krb5.conf is available than argument is required.
    :param searchbase: <class 'str'>
        - LDAP Base search path
          If None, will default to the associated root search base from the server
          located in the krb5.conf. If no krb5.conf is available than argument is required.
          i.e. DC=example,DC=com
    :param cacert: <class 'str'>
        - Root CA Certificate Path
          Required if tls=True and verify=True
    :param port: <class 'int'>
        - Port for ldap. Default 636
    :param tls: <class 'bool'>
        - Determines if connectivity should use TLS 1.2. Defaults to True
    :param username: <class 'str'>
        - FQDN of user to authenticate when not using Kerberos. Defaults to None.
    :param password: <class 'str'>
        - Password for user when not using Kerberos. If None will use getpass.
    :param properties: <class 'list'> or <class 'tuple'> or <class 'str'>
        - List of Properties to retrieve. If None will get distinguishedName and
          objectCategory only.
          i.e. properties=["ALL"] # For All Properties
          i.e. properties=["mail","cn"]
    :param verify: <class 'bool'>
        - Verifies the certificate of the server. Defaults to True.
    :return: <class 'list'> or None
        - Returns a list of dictionary objects representing each result.
    """
    if identity is not None:
        ldap_filter = f"(&(objectClass=computer)(|(cn={identity})(distinguishedName={identity})))"
    else:
        if filter is not None:
            ldap_filter = f"(&(objectClass=computer)({filter}))"
        else:
            ldap_filter = None

    return get_adobject_raw(ldap_filter, server, searchbase, cacert, port, tls, username, password, properties, verify)


def get_adorganizationalunit(filter: str=None, identity: str=None, server: str = None,
                 searchbase: str = None, cacert: str = None, port: int = 636,
                 tls: bool = True, username: str = None, password: str = None,
                 properties: list = None, verify: bool = True) -> list:
    """
    Gets AD OrganizationalUnit Object(s).
    :param filter: <class 'str'>
        - The specific ldap filter to query. This parameter is required.
    :param identity: <class 'str'>
        - Can be a CN, DistinguishedName
    :param server: <class 'str'>
        - The Active Directory Domain Controller to Query
          If None, will Default to the Default Domain server in the krb5.conf.
          If no krb5.conf is available than argument is required.
    :param searchbase: <class 'str'>
        - LDAP Base search path
          If None, will default to the associated root search base from the server
          located in the krb5.conf. If no krb5.conf is available than argument is required.
          i.e. DC=example,DC=com
    :param cacert: <class 'str'>
        - Root CA Certificate Path
          Required if tls=True and verify=True
    :param port: <class 'int'>
        - Port for ldap. Default 636
    :param tls: <class 'bool'>
        - Determines if connectivity should use TLS 1.2. Defaults to True
    :param username: <class 'str'>
        - FQDN of user to authenticate when not using Kerberos. Defaults to None.
    :param password: <class 'str'>
        - Password for user when not using Kerberos. If None will use getpass.
    :param properties: <class 'list'> or <class 'tuple'> or <class 'str'>
        - List of Properties to retrieve. If None will get distinguishedName and
          objectCategory only.
          i.e. properties=["ALL"] # For All Properties
          i.e. properties=["mail","cn"]
    :param verify: <class 'bool'>
        - Verifies the certificate of the server. Defaults to True.
    :return: <class 'list'> or None
        - Returns a list of dictionary objects representing each result.
    """
    organizationalunit_objects_raw = get_adorganizationalunit_raw(filter, identity, server, searchbase, cacert, port, tls, username, password,
                                      properties, verify)
    organizationalunits = []
    for organizationalunit_raw in organizationalunit_objects_raw:
        organizationalunits.append(ADOrganizationalUnit(organizationalunit_raw))

    return None if len(organizationalunits) == 0 else organizationalunits


def get_adorganizationalunit_raw(filter: str=None, identity: str=None, server: str = None,
                 searchbase: str = None, cacert: str = None, port: int = 636,
                 tls: bool = True, username: str = None, password: str = None,
                 properties: list = None, verify: bool = True) -> list:
    """
    Gets AD OrganizationalUnit Object(s) raw data.
    :param filter: <class 'str'>
        - The specific ldap filter to query. This parameter is required.
    :param identity: <class 'str'>
        - Can be a CN, DistinguishedName
    :param server: <class 'str'>
        - The Active Directory Domain Controller to Query
          If None, will Default to the Default Domain server in the krb5.conf.
          If no krb5.conf is available than argument is required.
    :param searchbase: <class 'str'>
        - LDAP Base search path
          If None, will default to the associated root search base from the server
          located in the krb5.conf. If no krb5.conf is available than argument is required.
          i.e. DC=example,DC=com
    :param cacert: <class 'str'>
        - Root CA Certificate Path
          Required if tls=True and verify=True
    :param port: <class 'int'>
        - Port for ldap. Default 636
    :param tls: <class 'bool'>
        - Determines if connectivity should use TLS 1.2. Defaults to True
    :param username: <class 'str'>
        - FQDN of user to authenticate when not using Kerberos. Defaults to None.
    :param password: <class 'str'>
        - Password for user when not using Kerberos. If None will use getpass.
    :param properties: <class 'list'> or <class 'tuple'> or <class 'str'>
        - List of Properties to retrieve. If None will get distinguishedName and
          objectCategory only.
          i.e. properties=["ALL"] # For All Properties
          i.e. properties=["mail","cn"]
    :param verify: <class 'bool'>
        - Verifies the certificate of the server. Defaults to True.
    :return: <class 'list'> or None
        - Returns a list of dictionary objects representing each result.
    """
    if identity is not None:
        ldap_filter = f"(&(objectClass=organizationalUnit)(|(cn={identity})(distinguishedName={identity})))"
    else:
        if filter is not None:
            ldap_filter = f"(&(objectClass=organizationalUnit)({filter}))"
        else:
            ldap_filter = None

    return get_adobject_raw(ldap_filter, server, searchbase, cacert, port, tls, username, password, properties, verify)


def print_adobjects(adobjects: list):
    """
    Pretty Prints Objects from raw data to standard output
    :param adobjects: <class 'list'>
        - The objects to print
    """
    adobjects = validate_argument(adobjects, [list,tuple], "adobjects")
    for adobject in adobjects:
        print(ADObject(adobject))


def get_json(adobject: list) -> str:
    """
    Prints json string to standard output from raw data
    :param adobject: <class 'list'>
        - The objects to print
    """
    def custom_serializer(obj):
        if isinstance(obj, datetime):
            return str(obj)
        elif isinstance(obj, bytes):
            return base64.b64encode(obj).decode('utf-8')
        raise TypeError(f"Type {type(obj)} not serializable")

    validate_argument(adobject, [list,tuple], "adobject")
    return json.dumps(adobject, default=custom_serializer)


def process_common_arguments(parser: argparse.ArgumentParser):
    """
    Adds arguments to argpareser that are common amongst entry points.
    :param parser: <class 'ArgumentParser'>
    """
    validate_argument(parser, argparse.ArgumentParser, "parser")
    parser.add_argument("-server", type=str, help="The Active Directory Domain Controller to Query.")
    parser.add_argument("-cacert", type=str,
                        help="Path to the Root CA that issued the DC Cert. This is required if tls=True and "
                             "verify=True.")
    parser.add_argument("-searchbase", type=str, help="LDAP Base search path.")
    parser.add_argument("-port", type=int, help="Port for ldap. Default 636.")
    parser.add_argument("-notls", action="store_true",
                        help="Determines if connectivity should use TLS 1.2. Defaults to False.")
    parser.add_argument("-username", type=str, help="FQDN of user to authenticate when not using Kerberos.")
    parser.add_argument("-password", type=str,
                        help="Password for user when not using Kerberos. If None will use getpass.")
    parser.add_argument("-properties", type=str, help="List of Properties to retrieve.")
    parser.add_argument("-noverify", action="store_true",
                        help="Verifies the certificate of the server. Defaults to False.")
    parser.add_argument("-json", action="store_true", help="Output data as a JSON String Dump.")


def set_defaults(port: int, properties: list):
    """
    Sets default values for port and properties if None
    :param port: <class 'int'>
    :param properties: <class 'list'>
    :return: <class 'int'>, <class 'list'>
    """
    validate_argument(port, int, "port", nullable=True)
    validate_argument(properties, [list,tuple,str], "properties",nullable=True)
    port = 636 if port is None else port
    properties = None if properties is None else [prop.strip() for prop in properties.split(',') if prop.strip() != ""]
    return port, properties


def display_stdout(adobjects: list, json_flag: bool):
    """
    Print Objects to standard output
    :param adobjects: <class 'list'>
        - Raw data
    :param json_flag: <class 'bool'>
        - Pretty Print or JSON output
    """
    validate_argument(adobjects,[dict,list,tuple], "adobjects")
    validate_argument(json_flag, bool, "json_flag")
    if adobjects is not None:
        if json_flag:
            print(get_json(adobjects))
        else:
            print_adobjects(adobjects)


def main_getadorganizationalunit():
    """
    Main entry point for getting AD OrganizationalUnit
    """
    parser = argparse.ArgumentParser(description="Get Active Directory Organizational Unit Object.")
    parser.add_argument("-filter", type=str, help="The specific ldap filter to query.")
    parser.add_argument("-identity", type=str, help="Identity of the Organizational Unit object. Required if filter not present.")
    process_common_arguments(parser)
    args = parser.parse_args()

    port, properties = set_defaults(args.port, args.properties)
    adobj = get_adorganizationalunit_raw(filter=filter, identity=args.identity, server=args.server, searchbase=args.searchbase,
                           cacert=args.cacert, port=port, tls=(not args.notls), username=args.username,
                           password=args.password, properties=properties, verify=(not args.noverify))
    display_stdout(adobj, args.json)


def main_getadcomputer():
    """
    Main entry point for getting AD Computer
    """
    parser = argparse.ArgumentParser(description="Get Active Directory Computer Object.")
    parser.add_argument("-filter", type=str, help="The specific ldap filter to query.")
    parser.add_argument("-identity", type=str, help="Identity of the Computer object. Required if filter not present.")
    process_common_arguments(parser)
    args = parser.parse_args()

    port, properties = set_defaults(args.port, args.properties)
    adobj = get_adcomputer_raw(filter=filter, identity=args.identity, server=args.server, searchbase=args.searchbase,
                           cacert=args.cacert, port=port, tls=(not args.notls), username=args.username,
                           password=args.password, properties=properties, verify=(not args.noverify))
    display_stdout(adobj, args.json)


def main_getadgroup():
    """
    Main entry point for getting AD Group
    """
    parser = argparse.ArgumentParser(description="Get Active Directory Group Object.")
    parser.add_argument("-filter", type=str, help="The specific ldap filter to query.")
    parser.add_argument("-identity", type=str, help="Identity of the Group object. Required if filter not present.")
    process_common_arguments(parser)
    args = parser.parse_args()

    port, properties = set_defaults(args.port, args.properties)
    adobj = get_adgroup_raw(filter=filter, identity=args.identity, server=args.server, searchbase=args.searchbase,
                           cacert=args.cacert, port=port, tls=(not args.notls), username=args.username,
                           password=args.password, properties=properties, verify=(not args.noverify))
    display_stdout(adobj, args.json)


def main_getaduser():
    """
    Main entry point for getting AD User
    """
    parser = argparse.ArgumentParser(description="Get Active Directory User Object.")
    parser.add_argument("-filter", type=str, help="The specific ldap filter to query.")
    parser.add_argument("-identity", type=str, help="Identity of the User object. Required if filter not present.")
    process_common_arguments(parser)
    args = parser.parse_args()

    port, properties = set_defaults(args.port, args.properties)
    adobj = get_aduser_raw(filter=filter, identity=args.identity, server=args.server, searchbase=args.searchbase,
                           cacert=args.cacert, port=port, tls=(not args.notls), username=args.username,
                           password=args.password, properties=properties, verify=(not args.noverify))
    display_stdout(adobj, args.json)


def main():
    """
    Main Entry Point.
    """
    parser = argparse.ArgumentParser(description="Get Active Directory Object.")
    parser.add_argument("-filter", type=str, help="The specific ldap filter to query. This parameter is required.")
    process_common_arguments(parser)
    args = parser.parse_args()

    port, properties = set_defaults(args.port, args.properties)
    adobj = get_adobject_raw(filter=args.filter, server=args.server, searchbase=args.searchbase, cacert=args.cacert,
                         port=port, tls=(not args.notls), username=args.username, password=args.password,
                         properties=properties, verify=(not args.noverify))
    display_stdout(adobj, args.json)


if __name__ == "__main__":
    main()
