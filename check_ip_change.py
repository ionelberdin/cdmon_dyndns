from urllib import request

def get_ip():
    # FIXME: if this method fails, then it should try ipgetter2
    # The issue with ipgetter2 is that it takes much onger but
    # it's surely more robust
    with request.urlopen('https://ifconfig.me') as r:
        return r.read().decode('utf-8')

def check_ip_change():
    ip = get_ip()
    with open('ip.log') as f:
        # FIXME:go to last line without iterating through all of them 
        for line in f:
            pass
    last_ip = line.split(',')[1].strip('\n').strip()
    if (last_ip == ip):
        return False
    update_ip(ip)

def update_ip(ip):
    from datetime import datetime as dt
    from cdmon_dyndns import send_request
    from login_details import user, md5pass

    response = send_request(user, md5pass, ip)
    if not ('ok' in response):
        # FIXME: this should raise an alert
        return

    with open('ip.log', 'a') as f:
        f.writelines(['{},{}\n'.format(dt.today().strftime('%Y-%m-%d %H:%M:%S'),ip)])

if __name__ == '__main__':
    check_ip_change()
