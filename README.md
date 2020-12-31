# CDmon Dynamic DNS update
Update the Dynamic DNS service provided by CDmon (https//cdmon.com).

Explanation from CDmon about how to trigger Dynamic DNS update:
- https://ticket.cdmon.com/es/support/solutions/articles/7000005922-api-de-actualizaci%c3%b3n-de-ip-del-dns-gratis-din%c3%a1mico?set_locale=2&_ga=2.261179533.1883837017.1609418615-1272155764.1496775312

Dependencies:
* ```Python 3.x```
* ```ipgetter2 library```

Use cases:
1. Check if your login details work:
```bash
$ python3 cdmon_dyndns.py -c
``` 
You'll be prompted to enter user name and password
If you'd rather enter those details directly:
```bash
$ python3 cdmon_dyndns.py -c -u {username} -p {password}
```
Where ```{username}``` and ```{password}``` are placeholders for your actual login details.

2. Store your login details in a local file.
Note: password will be only stored in MD5 encrypted manner.
```bash
$ python3 cdmon_dyndns.py -cs [-u {username} -p {password}]
```
```-c``` will prevent the script from requesting an IP address
The block between backets is optional.

3. Update the IP address using your previously stored login details:
```bash
$ python3 cdmon_dyndns.py -lg
```
The IP address will be automatically retrieved.

4. Update to an IP address of your choice:
```bash
$ python3 cdmon_dyndns.py -i {IP_address}
```

5. Print request URL using verbose mode:
```bash
$ python3 cdmon_dyndns.py -v
```

6. Send the request from a different script:
```python
from cdmon_dyndns import send_request
send_request(user, md5pass)  # this will only check if the login succeeds
send_request(user, md5pass, ip)  # this will also try to update the IP
```

Please note that several other option combinations may also be possible.
You may get more information about the available options by either reading
the ```cdmon_dyndns.py``` script, or by invoking its argparse help:
```bash
$ python3 cdmon_dyndns.py -h
```
or:

```bash
$ python3 cdmon_dyndns.py --help
```
