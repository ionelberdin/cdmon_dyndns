import argparse
import hashlib
import urllib

from ipgetter2 import ipgetter1 as ipgetter

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


def save_login_details(user, md5pass):
    with open('login_details.py', 'w') as f:
        f.writelines("user = '{}'\nmd5pass = '{}'".format(user, md5pass))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--login_details', default=False,
                        action='store_true', help="Use stored login details")
    parser.add_argument('-c', '--check_login', default=False,
                        action='store_true', help="Check login details")
    parser.add_argument('-g', '--get_ip', default=False,
                        action='store_true', help="tails")
    parser.add_argument('-u', '--user', default=None,
                        help="User name.")
    parser.add_argument('-p', '--passwd', default=None,
                        help="Unecrypted password.")
    parser.add_argument('-m', '--md5pass', default=None,
                        help="MD5 ecrypted password.")
    parser.add_argument('-i', '--ip', default=None,
                        help="IP address.")
    parser.add_argument('-s', '--save_login_details', default=False,
                        action='store_true', help="Save login details.")
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

    if args.save_login_details:
        save_login_details(**kwargs)

    ip = None
    if args.ip is not None:
        ip = args.ip
    elif args.get_ip:
        ip = ipgetter.myip()
    elif not args.check_login:
        ip = input("Enter an IP address:")
    kwargs['ip'] = ip if ip != '' else None

    kwargs['verbose'] = args.verbose

    send_request(**kwargs)

