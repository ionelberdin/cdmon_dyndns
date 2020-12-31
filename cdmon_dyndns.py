"""
Update the Dynamic DNS service provided by CDmon (https//cdmon.com).

Explanation from CDmon about how to trigger Dynamic DNS update:
https://ticket.cdmon.com/es/support/solutions/articles/7000005922-api-de-actualizaci%c3%b3n-de-ip-del-dns-gratis-din%c3%a1mico?set_locale=2&_ga=2.261179533.1883837017.1609418615-1272155764.1496775312

Dependencies:
    Python 3.x
    ipgetter2 library

Use cases:
    1. Check if your login details work:
    >>> python3 cdmon_dyndns.py -c
    
    You'll be prompted to enter user name and password
    If you'd rather enter those details directly:
    >>> python3 cdmon_dyndns.py -c -u {username} -p {password}

    Where {username} and {password} are placeholders for your actual login details.

    2. Store your login details in a local file.
    Note: password will be only stored in MD5 encrypted manner.
    >>> python3 cdmon_dyndns.py -cs [-u {username} -p {password}]

    -c will prevent the script from requesting an IP address.
    The block between backets is optional.

    3. Update the IP address using your previously stored login details:
    >>> python3 cdmon_dyndns.py -lg

    The IP address will be automatically retrieved.

    4. Update to an IP address of your choice:
    >>> python3 cdmon_dyndns.py -i {IP_address}

    5. Print request URL using verbose mode:
    >>> python3 cdmon_dyndns.py -v

    6. Send the request from a different script:
    >>> from cdmon_dyndns import send_request
    >>> send_request(user, md5pass)  # this will only check if the login succeeds
    >>> send_request(user, md5pass, ip)  # this will also try to update the IP

Please note that several other option combinations may also be possible.
You may get more information about the available options by either reading
this script, or by invoking the argparse help:
    >>> python3 cdmon_dyndns.py -h

    or:
    >>> python3 cdmon_dyndns.py --help
"""

# Standard library imports
import argparse
import hashlib
import urllib

# 3rd party librariy impots
from ipgetter2 import ipgetter1 as ipgetter

# Global constants
CDMON_URL = 'https://dinamico.cdmon.org/onlineService.php?{options}'

def send_request(user, md5pass, ip=None, verbose=False):

    # build options string
    options = 'enctype=MD5&n={}&p={}'.format(user, md5pass)
    if ip is not None:
        options += '&cip={}'.format(ip) 

    # generate full url for request
    url = CDMON_URL.format(options=options)
    
    if verbose:
        print(url)

    # send request
    with urllib.request.urlopen(url) as response:
        print(response.read())

def get_ip():
    return ipgetter.myip()

def store_login_details(user, md5pass):
    with open('login_details.py', 'w') as f:
        f.writelines("user = '{}'\nmd5pass = '{}'".format(user, md5pass))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--login_details', default=False,
                        action='store_true', help="Use stored login details.")
    parser.add_argument('-c', '--check_login', default=False,
                        action='store_true', help="Check login details, \
                        don't update IP.")
    parser.add_argument('-g', '--get_ip', default=False,
                        action='store_true', help="Get IP automatically.")
    parser.add_argument('-u', '--user', default=None,
                        help="Provide user name for authentication.")
    parser.add_argument('-p', '--passwd', default=None,
                        help="Provide raw password for authentication.")
    parser.add_argument('-m', '--md5pass', default=None,
                        help="Provide MD5 ecrypted password for authentication.")
    parser.add_argument('-i', '--ip', default=None,
                        help="Provide IP address to be used for the update.")
    parser.add_argument('-s', '--store_login_details', default=False,
                        action='store_true', help="Store login details.")
    parser.add_argument('-v', '--verbose', default=False,
                        action='store_true', help="Run script in verbose mode.")
    args = parser.parse_args()

    kwargs = {'user': None, 'md5pass': None}
    if args.login_details:
        from login_details import user, md5pass
    else:
        user = args.user or input("Enter user name:")
        if args.md5pass is not None:
            md5pass = args.md5pass
        else:
            passwd = args.passwd or input("Enter user password:")
            md5pass = hashlib.md5(passwd.encode('utf8')).hexdigest()
            del(passwd, args.passwd)

    kwargs['user'] = user
    kwargs['md5pass'] = md5pass

    if args.store_login_details:
        store_login_details(**kwargs)

    ip = None
    if args.ip is not None:
        ip = args.ip
    elif args.get_ip:
        ip = get_ip()
    elif not args.check_login:
        ip = input("Enter an IP address:")
    kwargs['ip'] = ip if ip != '' else None

    kwargs['verbose'] = args.verbose

    send_request(**kwargs)
